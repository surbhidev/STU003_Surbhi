# CTF Challenge: Book Review Analysis

## Approach Summary
This solves a 3-step Capture the Flag challenge involving the detection of manipulated book reviews in a dataset.

### Step 1: Find Manipulated Book (FLAG1)
- Computed SHA256 hash of student ID "STU003" to get `70CBAEF1`
- Identified books with suspicious criteria: `rating_number = 1234` and `average_rating = 5.0`
- Selected the first matching book from 150 candidates
- Extracted first 8 non-space characters from the book title
- Computed FLAG1 as SHA256 hash of these characters

### Step 2: Identify Fake Review (FLAG2)
- Searched all reviews for the student hash `70CBAEF1`
- Located the injected fake review with `parent_asin: nan`
- FLAG2 is simply the formatted student hash

### Step 3: Explain Authenticity (FLAG3)
- Analyzed genuine reviews of the target book
- Identified suspicious reviews using criteria: 5-star ratings, short length (<50 words), excessive superlatives
- Performed word frequency analysis on genuine reviews
- Extracted top 3 most frequent substantive words
- Combined words with numeric student ID and computed SHA256 hash for FLAG3

### Technical Implementation
- **Data Processing**: Pandas for efficient CSV handling
- **Text Analysis**: Regular expressions and Counter for word frequency
- **Feature Engineering**: Review length, word count, superlative detection
- **Output Generation**: Separate flag files and consolidated summary

## File Structure
- `solver.py` - Main solution script
- `FLAG1.txt` - Contains FLAG1 value
- `FLAG2.txt` - Contains FLAG2 value  
- `FLAG3.txt` - Contains FLAG3 value
- `flags.txt` - Consolidated flags file
- `README.md` - This approach summary
- `reflection.md` - Detailed methodology reflection

## Requirements
- pandas
- hashlib
- re
- collections