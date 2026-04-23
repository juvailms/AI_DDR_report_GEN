from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import fitz
import os
from llm_agent import extract_observations
from ddr_generate import generate_ddr_report


inspection_pdf  = "Sample_report.pdf"
thermal_pdf = "Thermal Images.pdf"

def extract_pdf_data(pdf_path, prefix):
    doc = fitz.open(pdf_path)

    all_text = ""
    image_paths = []

    os.makedirs("images", exist_ok=True)

    for page_index, page in enumerate(doc):
        all_text += page.get_text()

        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            image_name = f"images/{prefix}_page{page_index+1}_img{img_index+1}.png"

            with open(image_name, "wb") as f:
                f.write(image_bytes)

            image_paths.append(image_name)

    return all_text, image_paths


processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def generate_caption(image_path):
    image = Image.open(image_path).convert("RGB")

    inputs = processor(image, return_tensors="pt")
    # out = model.generate(**inputs)
    out = model.generate(**inputs, max_new_tokens=50)

    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption

def main():

    print("Pipeline started")

    print("Extracting Inspection Report...")
    inspection_text, inspection_images = extract_pdf_data(inspection_pdf, "insp")

    print("Extracting Thermal Report...")
    thermal_text, thermal_images = extract_pdf_data(thermal_pdf, "therm")

    print(f"Inspection Text length: {len(inspection_text)}")
    print(f"Inspection Images found: {len(inspection_images)}")

    print(f"thermal text: {len(thermal_text)}")
    print(f"thermal images found: {len(thermal_images)}")

    print("Generating BLIP captions...")
    
    all_images = inspection_images + thermal_images

    captions = []
    for img in all_images[:50]:
        cap = generate_caption(img)
        captions.append({"image": img, "caption": cap})
        print(f"Caption: {cap}")

    combined_text = f"""
    INSPECTION REPORT:
    {inspection_text[:3000]}

    THERMAL REPORT:
    {thermal_text[:2000]}"""

    print("Running LLM...")
    result = extract_observations(combined_text, captions)

    print("\nFINAL OUTPUT:\n")
    print(result)

    report = generate_ddr_report(result)
    with open("DDR_Report.md", "w", encoding="utf-8") as f:
        f.write(report)


if __name__ == "__main__":
    main()