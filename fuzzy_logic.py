
class FuzzyCS2:
    def __init__(self):
        # Membership ranges (Refined for CS2 Meta)
        self.adr_low_range = [0, 0, 45, 65]
        self.adr_normal_range = [55, 75, 95]
        self.adr_high_range = [85, 105, 200, 200]
        
        self.kd_small_range = [0, 0, 0.7, 1.0]
        self.kd_medium_range = [0.8, 1.1, 1.4]
        self.kd_large_range = [1.2, 1.6, 3.0, 3.0] # Fixed typo from 12 to 1.2
        
        self.rating_bronze_range = [0, 0, 30, 50]
        self.rating_silver_range = [40, 55, 70]
        self.rating_gold_range = [65, 80, 90]
        self.rating_mvp_range = [92, 100, 100, 100]

    def trapezoid(self, x, a, b, c, d):
        # Handle shoulders and boundaries correctly
        if a == b and x <= a: return 1.0
        if c == d and x >= c: return 1.0
        if x <= a or x >= d: return 0.0
        if x >= b and x <= c: return 1.0
        if a < x < b: return (x - a) / (b - a)
        if c < x < d: return (d - x) / (d - c)
        return 0.0

    def triangle(self, x, a, b, c):
        if x <= a or x >= c: return 0.0
        if x == b: return 1.0
        if a < x < b: return (x - a) / (b - a)
        if b < x < c: return (c - x) / (c - b)
        return 0.0

    def get_adr_membership(self, adr):
        return {
            'Rendah': self.trapezoid(adr, *self.adr_low_range),
            'Normal': self.triangle(adr, *self.adr_normal_range),
            'Tinggi': self.trapezoid(adr, *self.adr_high_range)
        }

    def get_kd_membership(self, kd):
        return {
            'Kecil': self.trapezoid(kd, *self.kd_small_range),
            'Sedang': self.triangle(kd, *self.kd_medium_range),
            'Besar': self.trapezoid(kd, *self.kd_large_range)
        }

    def evaluate_rules(self, adr_m, kd_m):
        rules = []
        rules.append({'id': 1, 'if': 'ADR Tinggi & K/D Besar', 'then': 'MVP', 'val': min(adr_m['Tinggi'], kd_m['Besar'])})
        rules.append({'id': 2, 'if': 'ADR Tinggi & K/D Sedang', 'then': 'Gold', 'val': min(adr_m['Tinggi'], kd_m['Sedang'])})
        rules.append({'id': 3, 'if': 'ADR Tinggi & K/D Kecil', 'then': 'Silver', 'val': min(adr_m['Tinggi'], kd_m['Kecil'])})
        rules.append({'id': 4, 'if': 'ADR Normal & K/D Besar', 'then': 'Gold', 'val': min(adr_m['Normal'], kd_m['Besar'])})
        rules.append({'id': 5, 'if': 'ADR Normal & K/D Sedang', 'then': 'Silver', 'val': min(adr_m['Normal'], kd_m['Sedang'])})
        rules.append({'id': 6, 'if': 'ADR Normal & K/D Kecil', 'then': 'Bronze', 'val': min(adr_m['Normal'], kd_m['Kecil'])})
        rules.append({'id': 7, 'if': 'ADR Rendah & K/D Besar', 'then': 'Silver', 'val': min(adr_m['Rendah'], kd_m['Besar'])})
        rules.append({'id': 8, 'if': 'ADR Rendah & K/D Sedang', 'then': 'Bronze', 'val': min(adr_m['Rendah'], kd_m['Sedang'])})
        rules.append({'id': 9, 'if': 'ADR Rendah & K/D Kecil', 'then': 'Bronze', 'val': min(adr_m['Rendah'], kd_m['Kecil'])})
        return rules

    def aggregate(self, rules):
        aggr = {'Bronze': 0, 'Silver': 0, 'Gold': 0, 'MVP': 0}
        for r in rules:
            aggr[r['then']] = max(aggr[r['then']], r['val'])
        return aggr

    def defuzzify(self, aggr):
        numerator = 0
        denominator = 0
        for z in range(0, 101, 1):
            mu_z = 0
            mu_z = max(mu_z, min(aggr['Bronze'], self.trapezoid(z, *self.rating_bronze_range)))
            mu_z = max(mu_z, min(aggr['Silver'], self.triangle(z, *self.rating_silver_range)))
            mu_z = max(mu_z, min(aggr['Gold'], self.triangle(z, *self.rating_gold_range)))
            mu_z = max(mu_z, min(aggr['MVP'], self.trapezoid(z, *self.rating_mvp_range)))
            
            numerator += z * mu_z
            denominator += mu_z
            
        if denominator == 0:
            # Fallback for extreme edges if needed
            return 0, 0, 0
        return numerator / denominator, numerator, denominator

    def calculate(self, adr, kd):
        adr_m = self.get_adr_membership(adr)
        kd_m = self.get_kd_membership(kd)
        rules = self.evaluate_rules(adr_m, kd_m)
        aggr = self.aggregate(rules)
        rating, num, den = self.defuzzify(aggr)
        
        return {
            'inputs': {'adr': adr, 'kd': kd},
            'fuzzification': {'adr': adr_m, 'kd': kd_m},
            'rules': rules,
            'aggregation': aggr,
            'defuzzification': {
                'rating': round(rating, 2),
                'numerator': round(num, 2),
                'denominator': round(den, 2)
            }
        }
