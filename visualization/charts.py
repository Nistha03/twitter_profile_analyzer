import os
from collections import Counter
from typing import List, Dict, Any
import matplotlib.pyplot as plt

class ChartGenerator:
    def __init__(self, output_dir: str = "outputs") -> None:
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_category_pie_chart(self, tweets_data: List[Dict[str, Any]], filename: str = "category_distribution.png") -> str:
        categories = [row['predicted_category'] for row in tweets_data if row['predicted_category']]
        if not categories:
            return ""
        
        counts = Counter(categories)
        sizes = list(counts.values())
        
        # Format labels to show name and count (e.g., "electronics (21)")
        legend_labels = [f"{cat} ({count})" for cat, count in counts.items()]

        # 1. Change to a taller figure (10x8) so there is vertical room for stacked rows
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # 2. Lift the bottom margin higher to make space for the vertical legend
        fig.subplots_adjust(bottom=0.4)
        
        # 3. Draw the pie slices (radius 0.8 keeps it nicely sized)
        wedges, _ = ax.pie(sizes, startangle=140, radius=0.8)
        
        # Title matching your image format
        plt.title("Tweet Category Distribution", fontweight='bold', fontsize=14, pad=20)
        
        # 4. MATCHING YOUR FRIEND'S CHART: 2 columns!
        ax.legend(wedges, legend_labels,
                  title="Categories",
                  loc="upper center",
                  bbox_to_anchor=(0.5, -0.05),
                  ncol=2,               # Set to 2 columns so it stacks them 5 rows deep
                  fontsize='small',     # Font size bumped up since they have more vertical room
                  frameon=True)
        
        # 1. Save the file silently into the output folder
        output_path = os.path.join(self.output_dir, filename)
        plt.savefig(output_path, bbox_inches='tight') 
        
        # 2. !!! THE MAGIC LINE !!! 
        # This tells your computer to instantly open up the interactive Matplotlib window on your desktop
        plt.show()
        
        return output_path