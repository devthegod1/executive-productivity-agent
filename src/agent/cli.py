import sys
from agent.core import ExecutiveProductivityAgent
from agent.config import config

def main():
    print("=" * 70)
    print("  EXECUTIVE PRODUCTIVITY AGENT — ARJUN MALHOTRA (VP SALES)")
    print(f"  Simulated Reference Time: {config.SIMULATED_NOW}")
    print("  Type your question, 'briefing' for daily briefing, or 'exit' to quit.")
    print("=" * 70)

    try:
        agent = ExecutiveProductivityAgent()
    except Exception as e:
        print(f"Initialization error: {e}")
        sys.exit(1)

    while True:
        try:
            user_input = input("\nArjun > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit", "q"):
                print("Exiting agent session.")
                break

            if user_input.lower() == "briefing":
                print("\n[Synthesizing Executive Briefing...]")
                resp = agent.generate_briefing()
            else:
                resp = agent.answer_question(user_input)

            print("\n--- CHIEF OF STAFF RESPONSE ---")
            print(resp.answer)

            if resp.citations:
                print("\n--- SOURCES CITED ---")
                for cite in resp.citations[:8]:
                    print(f"  * {cite}")

        except (KeyboardInterrupt, EOFError):
            print("\nExiting session.")
            break
        except Exception as e:
            print(f"\nError processing query: {e}")

if __name__ == "__main__":
    main()