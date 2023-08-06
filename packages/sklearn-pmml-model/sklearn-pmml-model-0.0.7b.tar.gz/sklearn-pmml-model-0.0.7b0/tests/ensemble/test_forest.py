from unittest import TestCase
import sklearn_pmml_model
from sklearn_pmml_model.ensemble import PMMLForestClassifier
from io import StringIO
import numpy as np
from os import path
import pandas as pd
from warnings import catch_warnings


BASE_DIR = path.dirname(sklearn_pmml_model.__file__)


class TestForest(TestCase):
  def test_invalid_model(self):
    with self.assertRaises(Exception) as cm:
      PMMLForestClassifier(pmml=StringIO("""
      <PMML xmlns="http://www.dmg.org/PMML-4_3" version="4.3">
        <DataDictionary>
          <DataField name="Class" optype="categorical" dataType="string">
            <Value value="setosa"/>
            <Value value="versicolor"/>
            <Value value="virginica"/>
          </DataField>
        </DataDictionary>
        <MiningSchema>
          <MiningField name="Class" usageType="target"/>
        </MiningSchema>
      </PMML>
      """))

    assert str(cm.exception) == 'PMML model does not contain MiningModel.'

  def test_invalid_segmentation(self):
    with self.assertRaises(Exception) as cm:
      PMMLForestClassifier(pmml=StringIO("""
      <PMML xmlns="http://www.dmg.org/PMML-4_3" version="4.3">
        <DataDictionary>
          <DataField name="Class" optype="categorical" dataType="string">
            <Value value="setosa"/>
            <Value value="versicolor"/>
            <Value value="virginica"/>
          </DataField>
        </DataDictionary>
        <MiningModel>
          <MiningSchema>
            <MiningField name="Class" usageType="target"/>
          </MiningSchema>
        </MiningModel>
      </PMML>
      """))

    assert str(cm.exception) == 'PMML model does not contain Segmentation.'

  def test_non_voting_ensemble(self):
    with self.assertRaises(Exception) as cm:
      PMMLForestClassifier(pmml=StringIO("""
      <PMML xmlns="http://www.dmg.org/PMML-4_3" version="4.3">
        <DataDictionary>
          <DataField name="Class" optype="categorical" dataType="string">
            <Value value="setosa"/>
            <Value value="versicolor"/>
            <Value value="virginica"/>
          </DataField>
        </DataDictionary>
        <MiningModel>
          <MiningSchema>
            <MiningField name="Class" usageType="target"/>
          </MiningSchema>
          <Segmentation multipleModelMethod="mean" />
        </MiningModel>
      </PMML>
      """))

    assert str(cm.exception) == 'PMML model ensemble should use majority vote.'

  def test_non_true_segment(self):
    with self.assertRaises(Exception), catch_warnings(record=True) as w:
      PMMLForestClassifier(pmml=StringIO("""
      <PMML xmlns="http://www.dmg.org/PMML-4_3" version="4.3">
        <DataDictionary>
          <DataField name="Class" optype="categorical" dataType="string">
            <Value value="setosa"/>
            <Value value="versicolor"/>
            <Value value="virginica"/>
          </DataField>
        </DataDictionary>
        <MiningModel>
          <MiningSchema>
            <MiningField name="Class" usageType="target"/>
          </MiningSchema>
          <Segmentation multipleModelMethod="majorityVote">
            <Segment>
              <False/>
            </Segment>
            <Segment>
              <True/>
            </Segment>
          </Segmentation>
        </MiningModel>
      </PMML>
      """))
    assert len(w) == 1

  def test_non_binary_tree(self):
    with self.assertRaises(Exception) as cm:
      PMMLForestClassifier(pmml=StringIO("""
      <PMML xmlns="http://www.dmg.org/PMML-4_3" version="4.3">
        <DataDictionary>
          <DataField name="Class" optype="categorical" dataType="string">
            <Value value="setosa"/>
            <Value value="versicolor"/>
            <Value value="virginica"/>
          </DataField>
        </DataDictionary>
        <MiningModel>
          <MiningSchema>
            <MiningField name="Class" usageType="target"/>
          </MiningSchema>
          <Segmentation multipleModelMethod="majorityVote">
            <Segment>
              <True/>
              <TreeModel splitCharacteristic="multiSplit" />
            </Segment>
          </Segmentation>
        </MiningModel>
      </PMML>
      """))

    assert str(cm.exception) == 'Sklearn only supports binary tree models.'

  def test_fit_exception(self):
    with self.assertRaises(Exception) as cm:
      pmml = path.join(BASE_DIR, '../models/categorical-rf.pmml')
      clf = PMMLForestClassifier(pmml)
      clf.fit(np.array([[]]), np.array([]))

    assert str(cm.exception) == 'Not supported.'


class TestAchmea(TestCase):
    def all_object_categorical(self, df):
        for feature in df.columns:
            if df[feature].dtype == 'object':
                df[feature] = pd.Categorical(df[feature].astype(str), ordered=False)

            if df[feature].dtype == 'int64' and df[feature].nunique() < 6:
                df[feature] = pd.Categorical(df[feature].astype(str), ordered=True)

    def cat_to_int(self, df):
        for feature in df.columns:
            if feature != 'betaald' and df[feature].dtype.name == 'category':
                df[feature] = df[feature].cat.codes

    def remove_outliers(self, df, outlierConstant):
        from scipy import stats
        columns = [column for column in df.columns if df[column].dtype.name != 'category']
        before = df.shape[0]
        mask = (np.abs(stats.zscore(df[columns])) < outlierConstant).all(axis=1)
        df = df[mask]
        after = df.shape[0]
        print(f'{before - after} outliers removed')
        return df

    def setUp(self):
        columns = ['hist_EIP_niet_betaald','hist_EIP_betaald','saldo_premie','saldo_schade','aanvullend','LABEL','leeftijd','aantal_aanmaning1','aantal_aanmaning2','aantal_aanmaning3','DST08','DST10','DST12','DST27','provincie']

        df_tr = pd.read_csv(path.join(BASE_DIR, '../models/EIPtrain_new.csv')).dropna().rename('train_{}'.format)
        df_te = pd.read_csv(path.join(BASE_DIR, '../models/EIPtest_new.csv')).dropna().rename('test_{}'.format)

        df = pd.concat((df_tr, df_te), sort=True)
        self.all_object_categorical(df)
        #df = self.remove_outliers(df, 3)
        #self.cat_to_int(df)
        #df = df.assign(DST09=1)

        df_tr = df.reindex(df_tr.index).dropna()
        df_te = df_te.drop(columns=['prob'])
        Xtr = df_tr[df_tr.columns.difference(['betaald'])][columns]
        ytr = pd.Series(pd.Categorical(df_tr["betaald"]))

        df_te = df.reindex(df_te.index).dropna()
        yte_proba = df_te['prob']
        df_te = df_te.drop(columns=['prob'])
        Xte = df_te[df_te.columns.difference(['betaald'])][columns]
        yte = pd.Series(pd.Categorical(df_te["betaald"]))
        self.test = Xte, yte, yte_proba

        self.clf = PMMLForestClassifier(pmml=path.join(BASE_DIR, "../models/EIPmodel_new2.pmml"))

    def test_score(self):
        Xte, yte, _ = self.test
        ref = 0.8835104042245552
        assert ref == self.clf.score(Xte, yte)

    def test_predict_proba(self):
        Xte, _, yte = self.test
        ref = np.array(yte).reshape(-1,1)
        ref = np.c_[ref, np.round(1 - ref, decimals=2)]

        result = self.clf.predict_proba(Xte)

        assert np.array_equal(ref, result)


class TestIrisForestIntegration(TestCase):
  def setUp(self):
    from sklearn.datasets import load_iris
    iris = load_iris()
    X = pd.DataFrame(iris.data)
    X.columns = np.array(['sepal_length', 'sepal_width', 'petal_length',
                          'petal_width'])
    y = pd.Series(np.array(np.array(['Iris-setosa', 'Iris-versicolor',
                                     'Iris-virginica']))[iris.target])
    y.name = "Class"
    self.test = X, y

    self.clf = PMMLForestClassifier(path.join(BASE_DIR, '../models/iris.pmml'))

  def test_predict_proba(self):
    Xte, _ = self.test
    ref = np.array([
        [1., 0., 0.],
        [0.995, 0.005, 0.],
        [1., 0., 0.],
        [1., 0., 0.],
        [1., 0., 0.],
        [1., 0., 0.],
        [1., 0., 0.],
        [1., 0., 0.],
        [1., 0., 0.],
        [1., 0., 0.],
        [1., 0., 0.],
        [1., 0., 0.],
        [1., 0., 0.],
        [1., 0., 0.],
        [0.985, 0.015, 0.],
        [0.995, 0.005, 0.],
        [1., 0., 0.],
        [1., 0., 0.],
        [0.995, 0.005, 0.],
        [1., 0., 0.],
        [0.995, 0.005, 0.],
        [1., 0., 0.],
        [1., 0., 0.],
        [1., 0., 0.],
        [1., 0., 0.],
        [0.99, 0.01, 0.],
        [1., 0., 0.],
        [0.995, 0.005, 0.],
        [0.995, 0.005, 0.],
        [1., 0., 0.],
        [1., 0., 0.],
        [0.995, 0.005, 0.],
        [1., 0., 0.],
        [1., 0., 0.],
        [1., 0., 0.],
        [1., 0., 0.],
        [0.98, 0.02, 0.],
        [1., 0., 0.],
        [1., 0., 0.],
        [1., 0., 0.],
        [1., 0., 0.],
        [0.98, 0.015, 0.005],
        [1., 0., 0.],
        [1., 0., 0.],
        [1., 0., 0.],
        [1., 0., 0.],
        [1., 0., 0.],
        [1., 0., 0.],
        [1., 0., 0.],
        [1., 0., 0.],
        [0., 0.995, 0.005],
        [0., 1., 0.],
        [0., 0.595, 0.405],
        [0., 0.995, 0.005],
        [0., 0.99, 0.01],
        [0., 0.995, 0.005],
        [0., 0.97, 0.03],
        [0.005, 0.805, 0.19],
        [0., 1., 0.],
        [0.005, 0.985, 0.01],
        [0., 0.95, 0.05],
        [0., 0.995, 0.005],
        [0., 0.985, 0.015],
        [0., 0.995, 0.005],
        [0., 1., 0.],
        [0., 1., 0.],
        [0., 0.995, 0.005],
        [0., 1., 0.],
        [0., 0.99, 0.01],
        [0., 0.995, 0.005],
        [0., 0.645, 0.355],
        [0., 1., 0.],
        [0., 0.76, 0.24],
        [0., 1., 0.],
        [0., 1., 0.],
        [0., 1., 0.],
        [0., 0.85, 0.15],
        [0., 0.025, 0.975],
        [0., 0.995, 0.005],
        [0., 0.995, 0.005],
        [0., 0.995, 0.005],
        [0., 0.995, 0.005],
        [0., 1., 0.],
        [0., 0.085, 0.915],
        [0.025, 0.96, 0.015],
        [0.01, 0.945, 0.045],
        [0., 1., 0.],
        [0., 0.995, 0.005],
        [0., 1., 0.],
        [0., 0.995, 0.005],
        [0., 0.98, 0.02],
        [0., 0.995, 0.005],
        [0., 0.99, 0.01],
        [0., 0.955, 0.045],
        [0., 1., 0.],
        [0., 1., 0.],
        [0., 1., 0.],
        [0., 1., 0.],
        [0., 0.99, 0.01],
        [0., 1., 0.],
        [0., 0., 1.],
        [0., 0.01, 0.99],
        [0., 0., 1.],
        [0., 0., 1.],
        [0., 0., 1.],
        [0., 0., 1.],
        [0., 0.245, 0.755],
        [0., 0., 1.],
        [0., 0.065, 0.935],
        [0., 0., 1.],
        [0., 0.01, 0.99],
        [0., 0., 1.],
        [0., 0.005, 0.995],
        [0., 0.055, 0.945],
        [0., 0.005, 0.995],
        [0., 0., 1.],
        [0., 0., 1.],
        [0., 0., 1.],
        [0., 0.015, 0.985],
        [0., 0.19, 0.81],
        [0., 0., 1.],
        [0., 0.11, 0.89],
        [0., 0., 1.],
        [0., 0.07, 0.93],
        [0., 0., 1.],
        [0., 0.005, 0.995],
        [0., 0.12, 0.88],
        [0., 0.035, 0.965],
        [0., 0., 1.],
        [0., 0.05, 0.95],
        [0., 0., 1.],
        [0., 0.005, 0.995],
        [0., 0., 1.],
        [0., 0.115, 0.885],
        [0., 0.09, 0.91],
        [0., 0., 1.],
        [0., 0., 1.],
        [0., 0., 1.],
        [0., 0.18, 0.82],
        [0., 0., 1.],
        [0., 0., 1.],
        [0., 0.005, 0.995],
        [0., 0.01, 0.99],
        [0., 0.005, 0.995],
        [0., 0., 1.],
        [0., 0., 1.],
        [0., 0.09, 0.91],
        [0., 0., 1.],
        [0., 0., 1.],
        [0., 0.025, 0.975]
    ])

    assert np.array_equal(ref, self.clf.predict_proba(Xte))

  def test_score(self):
    Xte, yte = self.test
    ref = 0.9866666666666667
    assert ref == self.clf.score(Xte, yte)


class TestCategoricalPimaForestIntegration(TestCase):
  def setUp(self):
    df = pd.read_csv(path.join(BASE_DIR, '../models/categorical-test.csv'))
    cats = np.unique(df['age'])
    df['age'] = pd.Categorical(df['age'], categories=cats)
    Xte = df.iloc[:, 1:]
    yte = df.iloc[:, 0]
    self.test = (Xte, yte)

    pmml = path.join(BASE_DIR, '../models/categorical-rf.pmml')
    self.clf = PMMLForestClassifier(pmml)

  def test_predict_proba(self):
    Xte, _ = self.test
    ref = np.array([
      [0.2200000000000000, 0.7800000000000000],
      [0.5800000000000000, 0.4200000000000000],
      [0.2200000000000000, 0.7800000000000000],
      [0.1800000000000000, 0.8200000000000000],
      [0.0800000000000000, 0.9200000000000000],
      [0.3000000000000000, 0.7000000000000000],
      [0.2600000000000000, 0.7400000000000000],
      [0.3600000000000000, 0.6400000000000000],
      [0.4000000000000000, 0.6000000000000000],
      [0.1600000000000000, 0.8400000000000000],
      [0.2200000000000000, 0.7800000000000000],
      [0.3000000000000000, 0.7000000000000000],
      [0.1400000000000000, 0.8600000000000000],
      [0.6400000000000000, 0.3600000000000000],
      [0.1800000000000000, 0.8200000000000000],
      [0.1800000000000000, 0.8200000000000000],
      [0.7600000000000000, 0.2400000000000000],
      [0.2400000000000000, 0.7600000000000000],
      [0.3400000000000000, 0.6600000000000000],
      [0.2800000000000000, 0.7200000000000000],
      [0.0800000000000000, 0.9200000000000000],
      [0.2000000000000000, 0.8000000000000000],
      [0.6800000000000000, 0.3200000000000000],
      [0.1200000000000000, 0.8800000000000000],
      [0.2200000000000000, 0.7800000000000000],
      [0.3600000000000000, 0.6400000000000000],
      [0.2000000000000000, 0.8000000000000000],
      [0.8600000000000000, 0.1400000000000000],
      [0.9399999999999999, 0.0600000000000000],
      [0.7200000000000000, 0.2800000000000000],
      [0.5600000000000001, 0.4400000000000000],
      [0.9800000000000000, 0.0200000000000000],
      [0.4400000000000000, 0.5600000000000001],
      [0.8800000000000000, 0.1200000000000000],
      [0.6600000000000000, 0.3400000000000000],
      [0.5000000000000000, 0.5000000000000000],
      [0.7400000000000000, 0.2600000000000000],
      [0.2600000000000000, 0.7400000000000000],
      [0.1600000000000000, 0.8400000000000000],
      [0.6800000000000000, 0.3200000000000000],
      [0.7600000000000000, 0.2400000000000000],
      [0.7400000000000000, 0.2600000000000000],
      [0.5600000000000001, 0.4400000000000000],
      [0.5400000000000000, 0.4600000000000000],
      [0.5200000000000000, 0.4800000000000000],
      [0.1400000000000000, 0.8600000000000000],
      [0.7600000000000000, 0.2400000000000000],
      [0.8200000000000000, 0.1800000000000000],
      [0.4400000000000000, 0.5600000000000001],
      [0.9200000000000000, 0.0800000000000000],
      [0.5600000000000001, 0.4400000000000000],
      [0.2800000000000000, 0.7200000000000000]
    ])
    assert np.array_equal(ref, self.clf.predict_proba(Xte))

  def test_score(self):
    Xte, yte = self.test
    ref = 0.7884615384615384
    assert ref == self.clf.score(Xte, yte)
