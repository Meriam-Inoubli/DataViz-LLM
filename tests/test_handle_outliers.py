import unittest
import pandas as pd
import numpy as np
from data.data_transformation import handle_outliers

class TestHandleOutliers(unittest.TestCase):

    def setUp(self):
        # Création d'un DataFrame d'exemple avec des valeurs aberrantes
        self.df = pd.DataFrame({
            'A': [1, 2, 3, 100, 5, 6, 7, 8],
            'B': [5, 4, 3, 2, 1, 0, -1, -100]
        })
        self.df_no_outliers = pd.DataFrame({
            'A': [1, 2, 3, 4, 5, 6, 7, 8],
            'B': [5, 4, 3, 2, 1, 0, -1, -2]
        })

    def test_handle_outliers_nothing(self):
        # Tester la stratégie "Nothing" (pas de transformation)
        result = handle_outliers(self.df, strategy="Nothing")
        self.assertTrue(np.allclose(result['A'], self.df['A']))
        self.assertTrue(np.allclose(result['B'], self.df['B']))
    
    def test_handle_outliers_log_transformation(self):
        # Tester la stratégie "Log_transformation"
        result = handle_outliers(self.df, strategy="Log_transformation")
        self.assertTrue(result['A'].iloc[3] > 0)  
        self.assertTrue(result['B'].iloc[7] > 0)  
        self.assertTrue(result['A'].iloc[0] == 1)  
        self.assertTrue(result['B'].iloc[6] == -1)  

    def test_handle_outliers_mean(self):
        # Tester la stratégie "Mean"
        result = handle_outliers(self.df, strategy="Mean")
        mean_A = self.df['A'].mean()
        mean_B = self.df['B'].mean()
        self.assertEqual(result['A'].iloc[3], mean_A)
        self.assertEqual(result['B'].iloc[7], mean_B)

    def test_handle_outliers_median(self):
        # Tester la stratégie "Median"
        result = handle_outliers(self.df, strategy="Median")
        # Vérifier que les valeurs aberrantes ont été remplacées par la médiane
        median_A = self.df['A'].median()
        median_B = self.df['B'].median()
        self.assertEqual(result['A'].iloc[3], median_A)
        self.assertEqual(result['B'].iloc[7], median_B)

    def test_handle_outliers_drop(self):
        # Tester la stratégie "Drop"
        result = handle_outliers(self.df, strategy="Drop")
        # Vérifier que la ligne avec la valeur aberrante a été supprimée
        self.assertNotIn(100, result['A'].values)
        self.assertNotIn(-100, result['B'].values)
        self.assertEqual(len(result), len(self.df) - 1)  # Vérifier qu'une ligne a été supprimée

    def test_handle_outliers_no_numeric_columns(self):
        # Tester avec un DataFrame sans colonnes numériques
        df_no_numeric = pd.DataFrame({
            'C': ['a', 'b', 'c', 'd'],
            'D': ['x', 'y', 'z', 'w']
        })
        result = handle_outliers(df_no_numeric, strategy="Median")
        self.assertTrue(result.equals(df_no_numeric))  # Aucun changement attendu
    
    def test_handle_outliers_no_outliers(self):
        # Tester un DataFrame sans valeurs aberrantes
        result = handle_outliers(self.df_no_outliers, strategy="Median")
        # Vérifier que les données restent inchangées
        self.assertTrue(np.allclose(result['A'], self.df_no_outliers['A']))
        self.assertTrue(np.allclose(result['B'], self.df_no_outliers['B']))

if __name__ == '__main__':
    unittest.main()
