import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv(override=True)


class GroqClient:

    def __init__(self, model: str = "llama-3.1-8b-instant"):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not set in environment.")

        self.client = Groq(api_key=api_key)
        self.model = model

    def generate(self, prompt: str, max_tokens: int = 256) -> str:
        """Return raw text output from Groq LLM."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            raise RuntimeError(f"Groq LLM Error: {e}")

    # def ask_json(self, prompt: str, max_tokens: int = 512):
    #     """Return parsed JSON from LLM output."""
    #     output = self.generate(prompt, max_tokens=max_tokens)

    #     try:
    #         return json.loads(output)
    #     except json.JSONDecodeError:
    #         # fallback: try to extract JSON substring
    #         try:
    #             cleaned = self._extract_json(output)
    #             return json.loads(cleaned)
    #         except:
    #             raise ValueError("LLM output was not valid JSON.\n" + output)

    def ask_json(self, prompt: str, max_tokens: int = 512):
        output = self.generate(prompt, max_tokens=max_tokens).strip()

        # Try direct JSON parsing first
        try:
            return json.loads(output)
        except:
            pass

        # --- FAILSAFE JSON RECOVERY ---
        # Extract all valid { ... } objects individually
        objects = []
        buf = ""
        depth = 0
        inside = False

        for ch in output:
            if ch == "{":
                inside = True
                depth += 1

            if inside:
                buf += ch

            if ch == "}":
                depth -= 1
                if depth == 0:
                    # Try parsing isolated object
                    try:
                        obj = json.loads(buf)
                        objects.append(obj)
                    except:
                        pass
                    buf = ""
                    inside = False

        if objects:
            return objects

        # If nothing valid was extracted
        raise ValueError(
            "LLM output was not valid JSON, even after recovery.\n\nRAW OUTPUT:\n" + output
        )


    def _extract_json(self, text: str) -> str:
        """Extract JSON substring from messy LLM output."""
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            return text[start:end+1]

        # maybe it's a list
        start = text.find("[")
        end = text.rfind("]")
        if start != -1 and end != -1:
            return text[start:end+1]

        raise ValueError("Could not extract JSON from text.")
