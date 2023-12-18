import streamlit as st
from joblib import load


presence_classifier = load('api/presence_classifier.joblib')
presence_vect = load('api/presence_vectorizer.joblib')
category_classifier = load('api/category_classifier.joblib')
category_vect = load('api/category_vectorizer.joblib')

def main():
    st.title("Dark Pattern Detection")

    
    tokens = st.text_area("Enter tokens (one per line):", "").split('\n')

    if st.button("Detect Dark Patterns"):
        output = detect_dark_patterns(tokens)
        st.json({"result": output})

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
