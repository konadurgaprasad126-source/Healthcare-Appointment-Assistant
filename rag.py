import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class HospitalRAG:

    def __init__(self, data_folder="data"):

        self.data_folder = data_folder
        self.documents = self.load_documents()

        if self.documents:

            self.vectorizer = TfidfVectorizer(
                stop_words="english"
            )

            self.matrix = self.vectorizer.fit_transform(
                [
                    document["text"]
                    for document in self.documents
                ]
            )

        else:
            self.vectorizer = None
            self.matrix = None

    def load_documents(self):

        documents = []

        if not os.path.exists(self.data_folder):
            return documents

        for filename in os.listdir(self.data_folder):

            if filename.endswith(".txt"):

                path = os.path.join(
                    self.data_folder,
                    filename
                )

                with open(
                    path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    text = file.read()

                documents.append({
                    "title": filename,
                    "text": text
                })

        return documents

    def retrieve(self, question, top_k=3):

        if not self.documents:
            return []

        question_vector = self.vectorizer.transform(
            [question]
        )

        similarity = cosine_similarity(
            question_vector,
            self.matrix
        ).flatten()

        indexes = similarity.argsort()[::-1][:top_k]

        results = []

        for index in indexes:

            if similarity[index] > 0:

                results.append({
                    "title":
                        self.documents[index]["title"],

                    "text":
                        self.documents[index]["text"],

                    "score":
                        float(similarity[index])
                })

        return results

    def answer(self, question):

        results = self.retrieve(question)

        if not results:

            return {
                "answer":
                    "Sorry, I could not find relevant "
                    "information in the hospital knowledge base.",

                "sources": []
            }

        answer = (
            "According to the hospital knowledge base:\n\n"
        )

        for result in results:

            answer += (
                f"### {result['title']}\n"
                f"{result['text']}\n\n"
            )

        return {
            "answer": answer,
            "sources": results
        }