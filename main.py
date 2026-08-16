# ============================================================
#  main.py  –  Entry point / command-line interface
# ============================================================
# Run this file to use the summarizer:
#     python main.py
#
# It will ask you step by step:
#   1. Where to get the text (file or type it in)
#   2. How many sentences for the summary
#   3. Which scoring method to use
#   4. Whether to save the output
# ============================================================

from summarizer   import (generate_summary, preprocess_text,
                           get_top_keywords, get_word_frequency)
from file_handler import (read_text_file, read_pdf_file,
                           save_as_txt, save_as_pdf)


# ── HELPER: pretty print a divider line ─────────────────────

def divider(char="─", length=60):
    print(char * length)


# ── STEP 1: GET INPUT TEXT ──────────────────────────────────

def get_input_text():
    """Ask the user how they want to provide text."""
    print("\n How would you like to provide the text?")
    print("  1  Type / paste text directly")
    print("  2  Load from a .txt file")
    print("  3 Load from a .pdf file")

    choice = input("\nEnter 1, 2, or 3: ").strip()

    if choice == "1":
        print("\nPaste your text below. When done, type END on a new line and press Enter:")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            lines.append(line)
        return "\n".join(lines)

    elif choice == "2":
        path = input("Enter the path to your .txt file: ").strip()
        return read_text_file(path)

    elif choice == "3":
        path = input("Enter the path to your .pdf file: ").strip()
        return read_pdf_file(path)

    else:
        print("[ERROR] Invalid choice. Defaulting to direct input.")
        return get_input_text()


# ── STEP 2: CHOOSE SUMMARY LENGTH ───────────────────────────

def get_summary_length():
    """Ask how many sentences the user wants in the summary."""
    try:
        n = int(input("\nHow many sentences in the summary? (default 3): ").strip() or "3")
        if n < 1:
            n = 1
        return n
    except ValueError:
        print("[WARNING] Invalid number, using 3.")
        return 3


# ── STEP 3: CHOOSE SCORING METHOD ───────────────────────────

def get_method():
    """Let the user pick which scoring method to use."""
    print("\n  Choose scoring method:")
    print("  1 – Frequency  (fast, simple)")
    print("  2 – TF-IDF     (smarter, penalizes common words)")
    print("  3 – Combined   (best results – default)")

    choice = input("Enter 1, 2, or 3: ").strip()
    mapping = {"1": "frequency", "2": "tfidf", "3": "combined"}
    return mapping.get(choice, "combined")


# ── STEP 4: SHOW ANALYTICS ──────────────────────────────────

def show_analytics(text, scores):
    """Display keyword analysis and sentence importance scores."""
    divider()
    print("📊 ANALYTICS")
    divider()

    # Keywords
    filtered_words = preprocess_text(text)
    keywords = get_top_keywords(filtered_words, top_n=10)

    print("\n Top 10 Keywords:")
    for i, (word, freq) in enumerate(keywords, 1):
        bar = "█" * min(freq, 40)          # simple bar chart in terminal
        print(f"  {i:>2}. {word:<20} {freq:>3}x  {bar}")

    # Sentence scores
    print("\n Sentence Importance Scores:")
    sorted_sentences = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for i, (sentence, score) in enumerate(sorted_sentences[:5], 1):
        short = sentence[:70] + "..." if len(sentence) > 70 else sentence
        print(f"  #{i} score={score:.4f}  \"{short}\"")


# ── STEP 5: SAVE OUTPUT ─────────────────────────────────────

def save_output(summary):
    """Ask the user if they want to save and in which format."""
    print("\n Save the summary?")
    print("  1 – Save as .txt")
    print("  2 – Save as .pdf")
    print("  3 – Both")
    print("  4 – Don't save")

    choice = input("Enter 1–4: ").strip()

    if choice in ("1", "3"):
        path = input("  TXT filename (default: summary_output.txt): ").strip() or "summary_output.txt"
        save_as_txt(summary, path)

    if choice in ("2", "3"):
        path = input("  PDF filename (default: summary_output.pdf): ").strip() or "summary_output.pdf"
        save_as_pdf(summary, path)


# ── MAIN ────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("   AI-POWERED DOCUMENT SUMMARIZATION SYSTEM")
    print("        Teyzix Core Internship – Task AI-INT-1")
    print("=" * 60)

    # ── Get text
    text = get_input_text()

    if not text or len(text.strip()) < 50:
        print("[ERROR] Text is too short or empty. Please try again.")
        return

    # ── Get preferences
    num_sentences = get_summary_length()
    method        = get_method()

    # ── Run summarization
    print("\n⏳ Summarizing...")
    summary, sentences, scores = generate_summary(text, num_sentences, method)

    # ── Show results
    divider("=")
    print(" ORIGINAL TEXT")
    divider("=")
    print(text[:500] + ("..." if len(text) > 500 else ""))   # show first 500 chars

    divider("=")
    print(f" SUMMARY  ({num_sentences} sentences, method={method})")
    divider("=")
    print(summary)

    print(f"\n  Compression: {len(text)} chars → {len(summary)} chars "
          f"({100 - int(len(summary)/len(text)*100)}% reduced)")

    # ── Analytics
    show_analytics(text, scores)

    # ── Save
    save_output(summary)

    print("\n Done! Thank you for using the AI Summarizer.")


if __name__ == "__main__":
    main()
