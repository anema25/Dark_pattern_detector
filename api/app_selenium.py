import streamlit as st
from joblib import load
from selenium import webdriver

presence_classifier = load('api/presence_classifier.joblib')
presence_vect = load('api/presence_vectorizer.joblib')
category_classifier = load('api/category_classifier.joblib')
category_vect = load('api/category_vectorizer.joblib')

def main():
    st.title("Dark Pattern Detection")

    url = st.text_input("Enter the URL of the website:", "")
    
    if st.button("Detect Dark Patterns"):
        tokens = get_tokens_from_url(url)
        output = detect_dark_patterns(tokens)
        st.json({"result": output})

def get_tokens_from_url(url):
    try:
        driver = webdriver.Chrome()  # Use appropriate webdriver for your browser
        driver.get(url)
        tokens = [token.lower() for token in driver.page_source.split()]
        return tokens
    except Exception as e:
        st.error(f"Error fetching content from URL: {e}")
        return []
    finally:
        driver.quit()

def detect_dark_patterns(tokens):
    output = []

    for token in tokens:
        result = presence_classifier.predict(presence_vect.transform([token]))
        if result == 'Dark':
            cat = category_classifier.predict(category_vect.transform([token]))
            output.append(cat[0])
        else:
            output.append(result[0])

    dark_patterns = [tokens[i] for i in range(len(output)) if output[i] == 'Dark']
    st.text("Detected Dark Patterns:")
    for d in dark_patterns:
        st.text(d)
    
    st.text(f"Number of Detected Dark Patterns: {len(dark_patterns)}")

    st.text("Debugging:")
    st.text(f"Output of presence classifier: {output}")
    
    return output

if __name__ == '__main__':
    main()

