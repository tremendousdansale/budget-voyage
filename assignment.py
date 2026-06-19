# travel_advisor.py
import os
from google import genai
from google.genai import types
from google.genai.errors import APIError

class TravelAdvisor:
    def __init__(self, api_key: str = None):
        # Fallback to environment variable if key isn't passed explicitly
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.client = None
       
        if self.api_key:
            # Initialize the standard Google GenAI Client
            self.client = genai.Client(api_key=self.api_key)

    def generate_advice(self, destination: str, total_budget: float, currency: str,
                        duration_days: int, remaining_budget: float, total_spent: float,
                        expense_summary: dict) -> str:
        """
        Gathers raw data from other modules, constructs a clean prompt,
        and requests tailored budget insights from Gemini.
        """
       
        # 1. Crafting the system instructions and user prompt (Prompt Engineering)
        system_instruction = (
            "You are an expert AI Travel Financial Advisor. Your job is to analyze a traveler's budget, "
            "current spending behavior, and destination to give highly practical, actionable advice. "
            "Keep your response structured, concise (under 200 words), and friendly yet direct."
        )
       
        user_prompt = f"""
        Please analyze my current travel spending and give me advice.
       
        Trip Details:
        - Destination: {destination}
        - Total Budget: {total_budget} {currency}
        - Trip Duration: {duration_days} days
        - Current Total Spent: {total_spent} {currency}
        - Remaining Budget: {remaining_budget} {currency}
       
        Current Expense Breakdown by Category:
        {expense_summary}
       
        Please provide:
        1. A quick assessment of my pacing (Am I burning money too fast?).
        2. Destination-specific budgeting tips for {destination}.
        3. One actionable recommendation based on my highest spending category.
        """

        # 2. Executing the API Call with Exception Handling
        if not self.client:
            return self._get_fallback_advice(destination, remaining_budget, currency)

        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7,  # Balanced between creative ideas and factual advice
                )
            )
            return response.text

        except APIError as e:
            print(f"[AI Error] Google GenAI API issue: {e}")
            return self._get_fallback_advice(destination, remaining_budget, currency)
        except Exception as e:
            print(f"[AI Error] Unexpected failure: {e}")
            return self._get_fallback_advice(destination, remaining_budget, currency)

    def _get_fallback_advice(self, destination: str, remaining_budget: float, currency: str) -> str:
        """Rule-based fallback if the API call fails or is unauthenticated."""
        return (
            f"🔮 [Local AI Advisor]: It looks like I am currently offline or the API key is missing. "
            f"However, looking at your destination ({destination}), always remember to watch out for hidden tourist taxes! "
            f"You have {remaining_budget} {currency} left. Try keeping daily food tracking strict to extend your wallet."
        )