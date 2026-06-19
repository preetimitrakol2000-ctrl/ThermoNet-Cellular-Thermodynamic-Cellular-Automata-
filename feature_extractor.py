class FeatureExtractor:
    @staticmethod
    def calculate_thermal_metrics(grid_flattened, width, height):
        """
        Computes statistical features from the flat grid data
        """
        total_temp = sum(grid_flattened)
        mean_temp = total_temp / len(grid_flattened)
        
        # Calculate a basic variance metric to represent spatial thermal gradient variance
        variance = sum((x - mean_temp) ** 2 for x in grid_flattened) / len(grid_flattened)
        
        return {
            "mean_temp": mean_temp,
            "thermal_variance": variance
        }
