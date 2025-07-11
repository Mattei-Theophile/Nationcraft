import os
import cv2
import numpy as np
import pytesseract
from PIL import Image
import re
import matplotlib.pyplot as plt


class NumberDetector:
    """A class to detect numbers in images using OCR."""

    def __init__(self, tesseract_path=None):
        """
        Initialize the NumberDetector.

        Args:
            tesseract_path: Path to Tesseract executable (for Windows)
        """
        # Configure tesseract path if provided (mainly for Windows)
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

        # Create output directory if it doesn't exist
        os.makedirs('output', exist_ok=True)

    def preprocess_image(self, image):
        """
        Preprocess the image to improve OCR accuracy.

        Args:
            image: Input image as numpy array

        Returns:
            Preprocessed image
        """
        # Convert to grayscale if image has channels
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 11, 2
        )

        # Noise removal using morphological operations
        kernel = np.ones((1, 1), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

        # Dilate to connect components
        dilated = cv2.dilate(opening, kernel, iterations=1)

        return dilated

    def extract_numbers(self, image, min_conf=0):
        """
        Extract numbers from an image.

        Args:
            image: Input image as numpy array
            min_conf: Minimum confidence level for OCR (0-100)

        Returns:
            List of detected numbers
        """
        # Preprocess the image
        processed = self.preprocess_image(image)

        # Use Tesseract to extract text with detailed info including confidence
        custom_config = f'--psm 6 outputbase digits --oem 3 -c tessedit_char_whitelist=0123456789'
        result = pytesseract.image_to_data(processed, config=custom_config, output_type=pytesseract.Output.DICT)

        # Extract numbers with confidence above threshold
        numbers = []
        for i in range(len(result['text'])):
            # Skip empty results or those below confidence threshold
            if not result['text'][i].strip() or int(float(result['conf'][i])) < min_conf:
                continue

            # Extract only numeric parts
            text = result['text'][i]
            numeric_text = re.sub(r'[^0-9]', '', text)

            if numeric_text:
                numbers.append({
                    'text': numeric_text,
                    'confidence': int(float(result['conf'][i])),
                    'bbox': (
                        result['left'][i],
                        result['top'][i],
                        result['width'][i],
                        result['height'][i]
                    )
                })

        return numbers, processed

    def visualize_results(self, image, numbers, processed=None):
        """
        Visualize the detected numbers on the image.

        Args:
            image: Original image
            numbers: List of detected numbers with bounding boxes
            processed: Preprocessed image (optional)

        Returns:
            Annotated image
        """
        # Create a copy to draw on
        annotated = image.copy()

        # Convert grayscale to BGR if needed
        if len(annotated.shape) == 2:
            annotated = cv2.cvtColor(annotated, cv2.COLOR_GRAY2BGR)

        # Draw bounding boxes and text
        for num in numbers:
            x, y, w, h = num['bbox']
            cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(
                annotated, f"{num['text']} ({num['confidence']}%)",
                (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
            )

        return annotated

    def process_image_file(self, image_path, min_conf=30, show_result=True):
        """
        Process a single image file.

        Args:
            image_path: Path to the image file
            min_conf: Minimum confidence threshold
            show_result: Whether to display the result

        Returns:
            List of detected numbers
        """
        try:
            # Read the image
            image = cv2.imread(image_path)
            if image is None:
                print(f"Error loading image: {image_path}")
                return []

            # Extract numbers
            numbers, processed = self.extract_numbers(image, min_conf)

            # Create visualization if numbers found
            if numbers:
                annotated = self.visualize_results(image, numbers, processed)

                # Save result
                filename = os.path.basename(image_path)
                base_name, ext = os.path.splitext(filename)
                output_path = os.path.join('output', f"{base_name}_detected{ext}")
                cv2.imwrite(output_path, annotated)

                # Display result
                if show_result:
                    plt.figure(figsize=(12, 8))

                    plt.subplot(131)
                    plt.title("Original")
                    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

                    plt.subplot(132)
                    plt.title("Processed")
                    plt.imshow(processed, cmap='gray')

                    plt.subplot(133)
                    plt.title("Detected Numbers")
                    plt.imshow(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))

                    plt.tight_layout()
                    plt.show()

                print(f"Detected numbers in {image_path}:")
                for num in numbers:
                    print(f"- {num['text']} (Confidence: {num['confidence']}%)")

            else:
                print(f"No numbers detected in {image_path}")

            return numbers

        except Exception as e:
            print(f"Error processing {image_path}: {str(e)}")
            return []

    def process_directory(self, directory_path, min_conf=30, extensions=('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff')):
        """
        Process all images in a directory.

        Args:
            directory_path: Path to the directory
            min_conf: Minimum confidence threshold
            extensions: Tuple of valid image extensions

        Returns:
            Dictionary with results for each image
        """
        results = {}

        if not os.path.exists(directory_path):
            print(f"Directory not found: {directory_path}")
            return results

        # Get all image files in the directory
        image_files = [
            os.path.join(directory_path, f) for f in os.listdir(directory_path)
            if os.path.isfile(os.path.join(directory_path, f)) and
               f.lower().endswith(extensions)
        ]

        if not image_files:
            print(f"No image files found in {directory_path}")
            return results

        print(f"Found {len(image_files)} image(s) in {directory_path}")

        # Process each image
        for image_path in image_files:
            print(f"\nProcessing: {image_path}")
            numbers = self.process_image_file(image_path, min_conf, show_result=True)
            results[image_path] = numbers

        return results


def main():
    # Path to Tesseract executable (required for Windows)
    # Change this according to your installation path if on Windows
    # tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # For Linux/Mac, Tesseract should be in the PATH, so we can leave it as None
    tesseract_path = None

    # Create detector
    detector = NumberDetector(tesseract_path)

    # Process all images in the test directory
    results = detector.process_directory('test', min_conf=30)

    # Print summary
    print("\n--- Summary ---")
    total_numbers = sum(len(nums) for nums in results.values())
    print(f"Processed {len(results)} images")
    print(f"Detected {total_numbers} numbers in total")


if __name__ == "__main__":
    main()