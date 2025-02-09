

    def meesho_converter(pdf_file, printer_type):
        try:
            input_pdf = fitz.open(pdf_file)
            cropped_pdf_bytes = BytesIO()
            new_pdf = fitz.open()

            # Get the dimensions of the first page to determine cropping
            first_page = input_pdf.load_page(0)
            page_width = first_page.rect.width

            # Set a higher DPI for better quality (e.g., 300 DPI)
            zoom_x = 3.0  # Horizontal scaling factor based on DPI
            zoom_y = 3.0  # Vertical scaling factor based on DPI
            mat = fitz.Matrix(zoom_x, zoom_y)  # Create a transformation matrix for scaling

            # Iterate through all pages in the PDF
            for page_num in range(len(input_pdf)):
                page = input_pdf[page_num]

                # Search for boundary texts meesho
                text_instances_meesho_1 = page.search_for(
                    "Includes discounts for your city and/or for online payments (as applicable)")
                text_instances_meesho_2 = page.search_for("If undelivered, return to:")

                if not (text_instances_meesho_1 and text_instances_meesho_2):
                    continue

                # Define the cropping box (remove the bottom part)
                left = 0  # X-coordinate of the top-left corner
                top = 0  # Y-coordinate of the top-left corner
                right = page_width  # X-coordinate of the bottom-right corner (full width)
                bottom = text_instances_meesho_1[0][3] + 20  # Adjust as needed

                # Crop the page by creating a transformation matrix with DPI scaling
                cropped_page = page.get_pixmap(matrix=mat, clip=fitz.Rect(left, top, right, bottom))

                # Convert to grayscale to reduce size (optional)
                if cropped_page.n < 5:  # Check if the image is not already grayscale
                    cropped_page = fitz.Pixmap(fitz.csGRAY, cropped_page)

                # Create a new page in the new PDF
                new_pdf.new_page(width=cropped_page.width, height=cropped_page.height)
                new_pdf[-1].insert_image(fitz.Rect(0, 0, cropped_page.width, cropped_page.height),
                                         pixmap=cropped_page, keep_proportion=True)

            if printer_type == 'thermal_printer':
                # Save the output PDF with optimization
                if len(new_pdf) > 0:
                    new_pdf.save(cropped_pdf_bytes, garbage=4, deflate=True)
                else:
                    print("No pages with text found. Output PDF not created.")

                cropped_pdf_bytes.seek(0)

                # Return the cropped PDF as a downloadable response
                response = HttpResponse(cropped_pdf_bytes, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="meesho_new.pdf"'
                return response