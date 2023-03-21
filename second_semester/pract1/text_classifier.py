import re
import nltk
from sklearn.datasets import load_files
import pickle

nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score


movie_data = load_files(r"D:\txt_sentoken")
X, y = movie_data.data, movie_data.target

documents = []

stemmer = WordNetLemmatizer()

for sen in range(0, len(X)):
    # Remove all the special characters
    document = re.sub(r'\W', ' ', str(X[sen]))

    # remove all single characters
    document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)

    # Remove single characters from the start
    document = re.sub(r'\^[a-zA-Z]\s+', ' ', document)

    # Substituting multiple spaces with single space
    document = re.sub(r'\s+', ' ', document, flags=re.I)

    # Removing prefixed 'b' for bit formats
    document = re.sub(r'^b\s+', '', document)

    # Converting to Lowercase
    document = document.lower()

    # Lemmatization
    document = document.split()

    document = [stemmer.lemmatize(word) for word in document]
    document = ' '.join(document)

    documents.append(document)

# здесь испольузуется алгоритм мешка слов для перевода слов текста в числа
# число слов 1500, другие будем считать редко втсречающимися и не подходящими для классификации, далее установлены границы
# встречаемости, минимум 5 источников должны содержать рассматриваемое слово, при этом оно должно встречаться максимум в 70% документов
# слова, которые встречаются очень редко -- уникальные, либо имена собственные, которые не несут никакой полезной информации
# слова, которые всречаются много и в каждом тексте -- тоже не информативны, так как являются общими
# далее передается набор стоп-слов из другой библиотеки для их исключения
vectorizer = CountVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
X = vectorizer.fit_transform(documents).toarray()

# далее рассчитывается значение TFIDF для найденных слов
# это значение позволяет объективно оценить частоту появления слов в тексте не для одного документа, а для всего набора.


tfidfconverter = TfidfTransformer()
X = tfidfconverter.fit_transform(X).toarray()

# далее датасет делится на набор для обучения и набор для тестирования в соотношении 80 на 20


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# в обучении используется модель случайного леса
classifier = RandomForestClassifier(n_estimators=1000, random_state=0)
classifier.fit(X_train, y_train)

# прогнозирование класса тестового набора
y_pred = classifier.predict(X_test)
print(y_pred)
# теперь нужно провести оценку точности полученной модели
# используется мера F, матрица замешательства и показатель точности

print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
print(accuracy_score(y_test, y_pred))

# сохранение модели для ее дальнейшего использования
# для сохранения модели используется pickle

with open('classifier', 'wb') as pickle_dump:
    pickle.dump(classifier, pickle_dump)

# для использования ее в других программах дамп модели можно будет загрузить так:
'''
with open('classifier', 'rb') as model:
    classifier_codel = pickle.load(model)
'''


