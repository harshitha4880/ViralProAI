from fpdf import FPDF
import datetime

class ReportGenerator:
    def generate_pdf(self, results, filename="virality_report.pdf"):
        """
        Creates a professional PDF report.
        """
        pdf = FPDF()
        pdf.add_page()
        
        # Header
        pdf.set_font("Arial", 'B', 20)
        pdf.set_text_color(40, 40, 100)
        pdf.cell(200, 20, "Instagram Virality Prediction Report", ln=True, align='C')
        
        pdf.set_font("Arial", 'I', 10)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(200, 10, f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='C')
        pdf.ln(10)

        # Core Metrics
        pdf.set_font("Arial", 'B', 16)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(200, 10, "1. Core Prediction Metrics", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.cell(200, 10, f"Virality Score: {results['virality_score']}/100", ln=True)
        pdf.cell(200, 10, f"Expected Likes: {results['likes']}", ln=True)
        pdf.cell(200, 10, f"Expected Comments: {results['comments']}", ln=True)
        pdf.cell(200, 10, f"Engagement Rate: {results['engagement_rate']}%", ln=True)
        pdf.ln(5)

        # Feature Analysis
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, "2. Feature Analysis", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.cell(200, 10, f"Caption Quality: {results['metadata']['nlp']['caption_quality']}%", ln=True)
        pdf.cell(200, 10, f"Hashtag Quality: {results['metadata']['hashtags']['quality_score']}%", ln=True)
        pdf.cell(200, 10, f"Media Brightness: {results['metadata']['media']['brightness_score']}", ln=True)
        pdf.cell(200, 10, f"Faces Detected: {results['metadata']['media']['face_count']}", ln=True)
        pdf.ln(5)

        # Recommendations
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, "3. Key Recommendations", ln=True)
        pdf.set_font("Arial", '', 12)
        for rec in results['recommendations']:
            pdf.multi_cell(200, 10, f"- [{rec['category']}] {rec['suggestion']} (Impact: {rec['impact']})")
        
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, "Final Strategy:", ln=True)
        pdf.set_font("Arial", 'I', 12)
        pdf.multi_cell(200, 10, results['strategy'])

        pdf.output(filename)
        return filename
