import pandas as pd
import hashlib
import re
from collections import Counter

def solver(student_id="STU003"):
    print(f"=== SOLVED FOR {student_id} ===")
    
    # Compute hash
    student_hash = hashlib.sha256(student_id.encode()).hexdigest()[:8].upper()
    print(f"Student Hash: {student_hash}")
    
    # Load data
    books_df = pd.read_csv('books.csv')
    reviews_df = pd.read_csv('reviews.csv')
    
    # STEP 1: Find fake review (FLAG2)
    print(f"\nSTEP 1: Finding fake review...")
    hash_reviews = reviews_df[reviews_df['text'].str.contains(student_hash, case=False, na=False)]
    
    if len(hash_reviews) == 0:
        print("Hash not found")
        return
    
    fake_review = hash_reviews.iloc[0]
    print(f"Fake review found: '{fake_review['text']}'")
    
    flag2 = f"FLAG2({student_hash})"
    print(f"FLAG2: {flag2}")
    
    # STEP 2: Find target book (FLAG1)
    print(f"\nSTEP 2: Finding target book...")
    target_books = books_df[
        (books_df['rating_number'] == 1234) & 
        (books_df['average_rating'] == 5.0)
    ]
    
    if len(target_books) == 0:
        print("No target books found")
        return
    
    # Use the first target book
    target_book = target_books.iloc[0]
    print(f"Target book: '{target_book['title']}'")
    
    # FLAG1
    title = target_book['title']
    first_8_chars = ''.join(title.split())[:8]
    flag1 = hashlib.sha256(first_8_chars.encode()).hexdigest()
    print(f"FLAG1: {flag1}")
    print(f"  (from '{title}' -> '{first_8_chars}')")
    
    # STEP 3: Analyze genuine reviews (FLAG3)
    print(f"\nSTEP 3: Analyzing genuine reviews...")
    book_reviews = reviews_df[reviews_df['parent_asin'] == target_book['parent_asin']]
    print(f"Total reviews: {len(book_reviews)}")
    
    if len(book_reviews) > 0:
        genuine_reviews = []
        for _, review in book_reviews.iterrows():
            text = str(review['text'])
            words = text.split()
            if len(words) > 30 and review['rating'] != 5:
                genuine_reviews.append(review)
        
        if len(genuine_reviews) == 0:
            genuine_reviews = book_reviews[book_reviews['rating'] != 5]
        
        if len(genuine_reviews) == 0:
            genuine_reviews = book_reviews
        
        print(f"Using {len(genuine_reviews)} genuine reviews")
        all_text = ' '.join([str(r['text']) for r in genuine_reviews])
        words = re.findall(r'\b[a-zA-Z]{4,}\b', all_text.lower())
        
        stop_words = {'this', 'that', 'with', 'have', 'from', 'they', 'what', 'when'}
        content_words = [w for w in words if w not in stop_words]
        
        word_freq = Counter(content_words)
        top_words = [word for word, count in word_freq.most_common(3)]
        print(f"Top 3 words: {top_words}")
        
        # FLAG3
        numeric_id = ''.join(filter(str.isdigit, student_id))
        concatenated = ''.join(top_words) + numeric_id
        flag3_hash = hashlib.sha256(concatenated.encode()).hexdigest()[:10]
        flag3 = f"FLAG3({flag3_hash})"
        print(f"FLAG3: {flag3}")
    else:
        flag3 = "FLAG3_NOT_FOUND"
    
    # Save individual flag files
    with open('FLAG1.txt', 'w') as f:
        f.write(flag1)
    
    with open('FLAG2.txt', 'w') as f:
        f.write(flag2)
    
    with open('FLAG3.txt', 'w') as f:
        f.write(flag3)
    
    # Save main flags.txt file
    with open('flags.txt', 'w') as f:
        f.write(f"FLAG1 = {flag1}\n")
        f.write(f"FLAG2 = {flag2}\n")
        f.write(f"FLAG3 = {flag3}\n")
    
    print(f"\nFiles created successfully!")
    print(f"  - FLAG1.txt: {flag1}")
    print(f"  - FLAG2.txt: {flag2}")
    print(f"  - FLAG3.txt: {flag3}")
    print(f"  - flags.txt: Main file with all flags")
    
    return flag1, flag2, flag3

if __name__ == "__main__":
    solver("STU003")