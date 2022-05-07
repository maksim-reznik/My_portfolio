import pandas

df = pandas.read_csv('titanic.csv')
p1 = (df[df['Pclass'] == 1]['Age'].mean())
p2 = (df[df['Pclass'] == 2]['Age'].mean())
p3 = (df[df['Pclass'] == 3]['Age'].mean())

df.drop(['PassengerId', 'Name', 'Ticket', 'Cabin'], axis=1, inplace=True)
df['Embarked'].fillna('S', inplace=True)
print(df['Embarked'].value_counts())
age_1 = df[df['Pclass'] == 1]['Age'].median()
age_2 = df[df['Pclass'] == 2]['Age'].median()
age_3 = df[df['Pclass'] == 3]['Age'].median()


def fill_age(row):
    if pandas.isnull(row['Age']):
        if row['Pclass'] == 1:
            return age_1
        elif row['Pclass'] == 2:
            return age_2

        else:
            return age_3


df['Age'] = df.apply(fill_age, axis=1)

print(pandas.get_dummies(df['Embarked']))


def dummies_sex(row):
    if row['Sex'] == 'male':
        return 0
    if row['Sex'] == 'female':
        return 1


df['Sex'] = df.apply(dummies_sex, axis=1)

df[list(pandas.get_dummies(df['Embarked']).columns)] = pandas.get_dummies(df['Embarked'])

df.drop('Embarked', axis=1, inplace=True)

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, accuracy_score

x = df.drop('Survived', axis=1)
y = df['Survived']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

classifier = KNeighborsClassifier(n_neighbors=3)
classifier.fit(x_train, y_train)

y_pred = classifier.predict(x_test)
percent = accuracy_score(y_test, y_pred) * 100

print(f'{percent} процентов правильных предсказаний')
