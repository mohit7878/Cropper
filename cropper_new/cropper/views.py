import tempfile
from io import BytesIO
import fitz
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import time

# # Create your views here.
# @csrf_exempt
# def cropper_main(request):
#     if request.method == 'POST':
#         pdf_file = request.FILES.get('pdf_file')
#         printer_type = request.POST.get('printer_type')
#
#
#         if pdf_file:
#             # Create a temporary file to save the uploaded PDF
#             with tempfile.NamedTemporaryFile(delete=False) as temp_pdf_file:
#                 # Write the contents of the uploaded file to the temporary file
#                 for chunk in pdf_file.chunks():
#                     temp_pdf_file.write(chunk)
#
#                 # Now, open the temporary file using fitz
#                 temp_pdf_file_path = temp_pdf_file.name
#                 input_pdf = fitz.open(temp_pdf_file_path)
#                 print(len(input_pdf))
#                 if len(input_pdf) > 1:
#
#                     page = input_pdf[1]
#                 else:
#                     page = input_pdf[0]
#
#                 # Search for boundary texts shiprocket
#                 text_instances_shiprocket_1 = page.search_for("DELIVER TO:")
#                 text_instances_shiprocket_2 = page.search_for(
#                     "THIS IS AN AUTO-GENERATED LABEL AND DOES NOT NEED SIGNATURE.")
#
#                 # Search for boundary texts flipkart
#                 text_instances_flipkart_1 = page.search_for("E-Kart Logistics")
#                 text_instances_flipkart_2 = page.search_for("AWB No.")
#
#                 # Search for boundary texts amazon
#                 text_instances_amazon_1 = page.search_for("Whether tax is payable under reverse charge")
#                 text_instances_amazon_2 = page.search_for("Amazon Seller Services Pvt. Ltd.")
#
#                 # Search for boundary texts meesho
#                 text_instances_meesho_1 = page.search_for("Tax is not payable on reverse charge basis.")
#                 text_instances_meesho_2 = page.search_for("If undelivered, return to:")
#
#                 if text_instances_shiprocket_1 and text_instances_shiprocket_2:
#                     pdf_type = 'Shiprocket'
#                 elif text_instances_flipkart_1 and text_instances_flipkart_2:
#                     pdf_type = 'Flipkart'
#                 elif text_instances_meesho_1 and text_instances_meesho_2:
#                     pdf_type = 'Meesho'
#                 elif text_instances_amazon_1 and text_instances_amazon_2:
#                     pdf_type = 'Amazon'
#                 else:
#                     json_data = {
#                         'id': 0,
#                         'msg': "Invalid PDF type. We only accept Shiprocket, Flipkart, Meesho, Amazon lable PDFs.",
#                     }
#                     return JsonResponse(json_data)
#
#                 if pdf_type == "Amazon":
#                     return amazon_converter(temp_pdf_file_path, printer_type)
#                 elif pdf_type == "Meesho":
#                     return meesho_converter(temp_pdf_file_path, printer_type)
#                 elif pdf_type == "Flipkart":
#                     a =flipkart_converter(temp_pdf_file_path, printer_type)
#                     print(a)
#                     return a
#                 elif pdf_type == "Shiprocket":
#                     return shiprocket_converter(temp_pdf_file_path, printer_type)
#                 else:
#                     json_data = {
#                         'id': 0,
#                         'msg': "Something Went Wrong!!! Please refresh the page."
#                     }
#                     return JsonResponse(json_data)
#
#                 # os.remove(temp_pdf_file_path)
#
#         else:
#             json_data = {
#                 'id': 0,
#                 'msg': "No file uploaded!!! Please Upload a File."
#             }
#             return JsonResponse(json_data)
#
#     return render(request, 'cropper_new.html')
#
#
# def amazon_converter(pdf_file, printer_type):
#     try:
#         input_pdf = fitz.open(pdf_file)
#
#         # Create a new PDF to store the cropped pages
#         cropped_pdf_bytes = BytesIO()
#         new_pdf = fitz.open()
#
#         # Extract odd-numbered pages (0-based indexing)
#         for page_num in range(input_pdf.page_count):
#             page = input_pdf[page_num]
#
#             # Search for boundary texts meesho
#             text_instances_amazon_1 = page.search_for("Whether tax is payable under reverse charge")
#             text_instances_amazon_2 = page.search_for("Amazon Seller Services Pvt. Ltd.")
#
#             if not (text_instances_amazon_1 and text_instances_amazon_2):
#                 new_pdf.insert_pdf(input_pdf, from_page=page_num, to_page=page_num)
#
#         if printer_type == 'thermal_printer':
#             # Save the output PDF
#             if len(new_pdf) > 0:
#                 new_pdf.save(cropped_pdf_bytes)
#             else:
#                 print("No pages with text found. Output PDF not created.")
#
#             # cropped_pdf_bytes.seek(0)
#             #
#             # # Return the new PDF as a downloadable response
#             # response = HttpResponse(cropped_pdf_bytes, content_type='application/pdf')
#             # response['Content-Disposition'] = 'attachment; filename="amazon_new.pdf"'
#             # return response
#             cropped_pdf_bytes.seek(0)
#             file_name = "amazon_new.pdf"
#             file_path = default_storage.save(file_name, ContentFile(cropped_pdf_bytes.read()))
#             download_url = default_storage.url(file_path)
#
#             return JsonResponse({'id': 1, 'download_url': download_url})
#
#
#         elif printer_type == 'inkjet_printer':
#             combined_pdf = inject_printer_common(new_pdf)
#
#             if len(combined_pdf) > 0:
#                 combined_pdf.save(cropped_pdf_bytes)
#             else:
#                 print("No pages with text found. Output PDF not created.")
#
#             cropped_pdf_bytes.seek(0)
#             file_name = "flipkart_new.pdf"
#             file_path = default_storage.save(file_name, ContentFile(cropped_pdf_bytes.read()))
#             download_url = default_storage.url(file_path)
#
#             return JsonResponse({'id': 1, 'download_url': download_url})
#
#
#         else:
#             json_data = {
#                 'id': 0,
#                 'msg': "Select Printer First."
#             }
#             return JsonResponse(json_data)
#
#     except Exception as e:
#         # Handle errors (e.g., invalid PDF file)
#         return HttpResponse(f"An error occurred: {str(e)}", status=400)
#
#
# def meesho_converter(pdf_file, printer_type):
#     try:
#         input_pdf = fitz.open(pdf_file)
#         cropped_pdf_bytes = BytesIO()
#         new_pdf = fitz.open()
#
#         # Thermal printer size in points (4x6 inches)
#         THERMAL_WIDTH = 288  # 4 inches = 288 points
#         THERMAL_HEIGHT = 432  # 6 inches = 432 points
#
#         # Set a higher DPI for better quality (e.g., 300 DPI)
#         zoom_x = 3.0  # Horizontal scaling factor based on DPI
#         zoom_y = 3.0  # Vertical scaling factor based on DPI
#         mat = fitz.Matrix(zoom_x, zoom_y)  # Create a transformation matrix for scaling
#
#         # Iterate through all pages in the PDF
#         for page_num in range(len(input_pdf)):
#             page = input_pdf[page_num]
#
#             # Search for boundary texts meesho
#             text_instances_meesho_1 = page.search_for(
#                 "Includes discounts for your city and/or for online payments (as applicable)")
#             text_instances_meesho_2 = page.search_for("If undelivered, return to:")
#
#             if not (text_instances_meesho_1 and text_instances_meesho_2):
#                 continue
#
#             # Define the cropping box (remove the bottom part)
#             left = 0  # X-coordinate of the top-left corner
#             top = 0  # Y-coordinate of the top-left corner
#             right = page.rect.width  # X-coordinate of the bottom-right corner (full width)
#             bottom = text_instances_meesho_1[0][3] + 20  # Adjust as needed
#
#             # Crop the page by creating a transformation matrix with DPI scaling
#             cropped_page = page.get_pixmap(matrix=mat, clip=fitz.Rect(left, top, right, bottom))
#
#             # Convert to grayscale to reduce size (optional)
#             if cropped_page.n < 5:  # Check if the image is not already grayscale
#                 cropped_page = fitz.Pixmap(fitz.csGRAY, cropped_page)
#
#             # Create a new page in the new PDF with thermal printer size (4x6 inches)
#             new_page = new_pdf.new_page(width=THERMAL_WIDTH, height=THERMAL_HEIGHT)
#
#             # Insert the cropped image into the thermal printer-sized page, resizing it to exactly fit
#             new_page.insert_image(
#                 fitz.Rect(0, 0, THERMAL_WIDTH, THERMAL_HEIGHT),  # Fill the entire thermal printer page
#                 pixmap=cropped_page,
#                 keep_proportion=False  # Disable aspect ratio preservation
#             )
#
#         if printer_type == 'thermal_printer':
#             # Save the output PDF with optimization
#             if len(new_pdf) > 0:
#                 new_pdf.save(cropped_pdf_bytes, garbage=4, deflate=True)
#             else:
#                 print("No pages with text found. Output PDF not created.")
#
#             # cropped_pdf_bytes.seek(0)
#             #
#             # # Return the cropped PDF as a downloadable response
#             # response = HttpResponse(cropped_pdf_bytes, content_type='application/pdf')
#             # response['Content-Disposition'] = 'attachment; filename="meesho_new.pdf"'
#             # return response
#             cropped_pdf_bytes.seek(0)
#             file_name = "meesho_new.pdf"
#             file_path = default_storage.save(file_name, ContentFile(cropped_pdf_bytes.read()))
#             download_url = default_storage.url(file_path)
#
#             return JsonResponse({'id': 1, 'download_url': download_url})
#
#         elif printer_type == 'inkjet_printer':
#             combined_pdf = inject_printer_common(new_pdf)
#
#             if len(combined_pdf) > 0:
#                 combined_pdf.save(cropped_pdf_bytes)
#             else:
#                 print("No pages with text found. Output PDF not created.")
#
#             cropped_pdf_bytes.seek(0)
#             file_name = "meesho_new.pdf"
#             file_path = default_storage.save(file_name, ContentFile(cropped_pdf_bytes.read()))
#             download_url = default_storage.url(file_path)
#
#             return JsonResponse({'id': 1, 'download_url': download_url})
#
#         else:
#             json_data = {
#                 'id': 0,
#                 'msg': "Select Printer First."
#             }
#             return JsonResponse(json_data)
#
#     except Exception as e:
#         # Handle errors (e.g., invalid PDF file)
#         return HttpResponse(f"An error occurred: {str(e)}", status=400)
#
#
# def flipkart_converter(pdf_file, printer_type):
#     try:
#         input_pdf = fitz.open(pdf_file)
#         cropped_pdf_bytes = BytesIO()
#         new_pdf = fitz.open()
#
#         # A4 dimensions in points (595 x 842)
#         A4_WIDTH = 595
#         A4_HEIGHT = 842
#
#         # Set a higher DPI for better quality (e.g., 300 DPI)
#         zoom_x = 3.0  # Horizontal scaling factor based on DPI
#         zoom_y = 3.0  # Vertical scaling factor based on DPI
#         mat = fitz.Matrix(zoom_x, zoom_y)  # Create a transformation matrix for scaling
#
#         # Iterate through all pages in the PDF
#         for page_num in range(len(input_pdf)):
#             page = input_pdf[page_num]
#
#             # Search for boundary texts
#             text_instances_flipkart_1 = page.search_for("E-Kart Logistics")
#             text_instances_flipkart_3 = page.search_for("QTY")
#             text_instances_flipkart_2 = page.search_for("Not for resale.")
#
#             if not (text_instances_flipkart_1 and text_instances_flipkart_2):
#                 print(f"Skipping page {page_num + 1}: boundary markers not found.")
#                 continue
#
#             # Define the cropping box
#             left = text_instances_flipkart_1[0].x0 - 30  # Left padding
#             top = text_instances_flipkart_1[0].y0 - 10   # Top padding
#             right = text_instances_flipkart_3[0].x1 + 8  # Right padding
#             bottom = text_instances_flipkart_2[0].y1 + 8 # Bottom padding
#
#             # Crop the page
#             crop_rect = fitz.Rect(left, top, right, bottom)
#             cropped_page = page.get_pixmap(matrix=mat, clip=crop_rect)
#
#             # Calculate scaling to fit A4
#             scale_x = A4_WIDTH / cropped_page.width
#             scale_y = A4_HEIGHT / cropped_page.height
#             scale = min(scale_x, scale_y)  # Maintain aspect ratio
#
#             # Create a new A4 page
#             new_page = new_pdf.new_page(width=A4_WIDTH, height=A4_HEIGHT)
#
#             # Calculate the position to center the cropped content on the A4 page
#             x_offset = (A4_WIDTH - (cropped_page.width * scale)) / 2
#             y_offset = (A4_HEIGHT - (cropped_page.height * scale)) / 2
#
#             # Insert the cropped and resized content into the A4 page
#             new_page.insert_image(
#                 fitz.Rect(x_offset, y_offset, A4_WIDTH - x_offset, A4_HEIGHT - y_offset),
#                 pixmap=cropped_page,
#             )
#
#         if printer_type == 'thermal_printer':
#             # Save the output PDF with compression
#             if len(new_pdf) > 0:
#                 new_pdf.save(cropped_pdf_bytes, deflate=True)  # Enable compression
#                 print("Output PDF saved successfully.")
#             else:
#                 print("No pages with text found. Output PDF not created.")
#
#
#             cropped_pdf_bytes.seek(0)
#             file_name = "flipkart_new.pdf"
#             file_path = default_storage.save(file_name, ContentFile(cropped_pdf_bytes.read()))
#             download_url = default_storage.url(file_path)
#
#             return JsonResponse({'id': 1, 'download_url': download_url})
#
#
#         elif printer_type == 'inkjet_printer':
#             combined_pdf = inject_printer_common(new_pdf)
#
#             if len(combined_pdf) > 0:
#                 combined_pdf.save(cropped_pdf_bytes)
#             else:
#                 print("No pages with text found. Output PDF not created.")
#
#             cropped_pdf_bytes.seek(0)
#             file_name = "flipkart_new.pdf"
#             file_path = default_storage.save(file_name, ContentFile(cropped_pdf_bytes.read()))
#             download_url = default_storage.url(file_path)
#
#             return JsonResponse({'id': 1, 'download_url': download_url})
#
#
#
#         else:
#             json_data = {
#                 'id': 0,
#                 'msg': "Select Printer First."
#             }
#             return JsonResponse(json_data)
#
#     except Exception as e:
#         # Handle errors (e.g., invalid PDF file)
#         return HttpResponse(f"An error occurred: {str(e)}", status=400)
#
#
# def shiprocket_converter(pdf_file, printer_type, left_padding=10, right_padding=10):
#     try:
#         # Open the input PDF
#         input_pdf = fitz.open(pdf_file)
#
#         # Create a new PDF to store the cropped pages
#         cropped_pdf_bytes = BytesIO()
#         new_pdf = fitz.open()
#
#         # A4 dimensions in points (1 point = 1/72 inch)
#         A4_WIDTH = 595.28
#         A4_HEIGHT = 841.89
#
#         for page_number in range(len(input_pdf)):
#             page = input_pdf[page_number]
#             page_width, page_height = page.rect.width, page.rect.height
#
#             # Search for boundary texts
#             text_instances_deliver_to = page.search_for("DELIVER TO:")
#             text_instances_label = page.search_for("THIS IS AN AUTO-GENERATED LABEL AND DOES NOT NEED SIGNATURE.")
#
#             if not (text_instances_deliver_to and text_instances_label):
#                 print(f"Required text not found on page {page_number + 1}. Skipping page.")
#                 continue
#
#             deliver_to_top = text_instances_deliver_to[0].y0
#             label_bottom = text_instances_label[0].y1 + 5
#
#             # Get all text blocks on the page
#             text_blocks = page.get_text("blocks")
#
#             # Split text blocks into left and right sections
#             mid_x = page_width / 2
#             left_blocks = [block for block in text_blocks if block[0] < mid_x]
#             right_blocks = [block for block in text_blocks if block[0] >= mid_x]
#
#             # Find leftmost and rightmost coordinates for each section
#             if left_blocks:
#                 left_crop_x = min(block[0] for block in left_blocks)
#                 left_crop_x = max(0, left_crop_x - left_padding)  # Apply left padding
#             else:
#                 left_crop_x = 0
#
#             if right_blocks:
#                 right_crop_x = max(block[2] for block in right_blocks)
#                 right_crop_x = min(right_crop_x + right_padding, page_width)  # Apply right padding
#             else:
#                 right_crop_x = page_width
#
#             # Define rectangles for left and right halves with all padding
#             left_rect = fitz.Rect(
#                 left_crop_x,
#                 deliver_to_top,
#                 page_width / 2,
#                 label_bottom
#             )
#
#             right_rect = fitz.Rect(
#                 page_width / 2,
#                 deliver_to_top,
#                 right_crop_x,
#                 label_bottom
#             )
#
#             # Extract left half of the page
#             left_page = fitz.open()
#             left_page.new_page(
#                 width=page_width / 2 - left_crop_x,
#                 height=label_bottom - deliver_to_top
#             )
#             left_page[0].show_pdf_page(left_page[0].rect, input_pdf, page_number, clip=left_rect)
#
#             # Extract right half of the page
#             right_page = fitz.open()
#             right_page.new_page(
#                 width=right_crop_x - page_width / 2,
#                 height=label_bottom - deliver_to_top
#             )
#             right_page[0].show_pdf_page(right_page[0].rect, input_pdf, page_number, clip=right_rect)
#
#             # Resize and insert left half into A4 page
#             if left_page[0].get_text():
#                 new_page = new_pdf.new_page(width=A4_WIDTH, height=A4_HEIGHT)
#                 new_page.show_pdf_page(
#                     fitz.Rect(0, 0, A4_WIDTH, A4_HEIGHT),  # Fill the entire A4 page
#                     left_page,  # Source PDF
#                     0,  # Page number
#                     clip=left_page[0].rect  # Use the entire left page
#                 )
#
#             # Resize and insert right half into A4 page
#             if right_page[0].get_text():
#                 new_page = new_pdf.new_page(width=A4_WIDTH, height=A4_HEIGHT)
#                 new_page.show_pdf_page(
#                     fitz.Rect(0, 0, A4_WIDTH, A4_HEIGHT),  # Fill the entire A4 page
#                     right_page,  # Source PDF
#                     0,  # Page number
#                     clip=right_page[0].rect  # Use the entire right page
#                 )
#
#             # Close temporary PDFs
#             left_page.close()
#             right_page.close()
#
#         if printer_type == 'thermal_printer':
#             # Save the output PDF
#             if len(new_pdf) > 0:
#                 new_pdf.save(cropped_pdf_bytes)
#                 print(f"Output PDF saved to {new_pdf}")
#             else:
#                 print("No pages with text found. Output PDF not created.")
#
#             # Seek to the beginning of the BytesIO object
#             # cropped_pdf_bytes.seek(0)
#             #
#             # # Return the cropped PDF as a downloadable response
#             # response = HttpResponse(cropped_pdf_bytes, content_type='application/pdf')
#             # response['Content-Disposition'] = 'attachment; filename="shiprocket_new.pdf"'
#             # return response
#             cropped_pdf_bytes.seek(0)
#             file_name = "shiprocket_new.pdf"
#             file_path = default_storage.save(file_name, ContentFile(cropped_pdf_bytes.read()))
#             download_url = default_storage.url(file_path)
#
#             return JsonResponse({'id': 1, 'download_url': download_url})
#
#
#
#
#         elif printer_type == 'inkjet_printer':
#             combined_pdf = inject_printer_common(new_pdf)
#
#             if len(combined_pdf) > 0:
#                 combined_pdf.save(cropped_pdf_bytes)
#             else:
#                 print("No pages with text found. Output PDF not created.")
#
#             cropped_pdf_bytes.seek(0)
#             file_name = "flipkart_new.pdf"
#             file_path = default_storage.save(file_name, ContentFile(cropped_pdf_bytes.read()))
#             download_url = default_storage.url(file_path)
#
#             return JsonResponse({'id': 1, 'download_url': download_url})
#
#         else:
#             json_data = {
#                 'id': 0,
#                 'msg': "Select Printer First."
#             }
#             return JsonResponse(json_data)
#
#     except Exception as e:
#         # Handle errors (e.g., invalid PDF file)
#         return HttpResponse(f"An error occurred: {str(e)}", status=400)
#
# def inject_printer_common(new_pdf):
#     # Create a new PDF to store the combined pages
#     combined_pdf = fitz.open()
#
#     # Define A4 page size in points (1 mm = 2.83465 points)
#     a4_width = 595  # 210 mm
#     a4_height = 842  # 297 mm
#
#     # Define the positions for the 4 quadrants
#     positions = [
#         (0, 0),  # Top-left
#         (a4_width / 2, 0),  # Top-right
#         (0, a4_height / 2),  # Bottom-left
#         (a4_width / 2, a4_height / 2),  # Bottom-right
#     ]
#
#     # Iterate through the new_pdf in chunks of 4 pages
#     for i in range(0, len(new_pdf), 4):
#         # Create a new A4 page in the output PDF
#         new_page = combined_pdf.new_page(width=a4_width, height=a4_height)
#
#         # Paste each of the 4 pages onto the new page
#         for j in range(4):
#             if i + j < len(new_pdf):
#                 page = new_pdf[i + j]
#
#                 # Define the target rectangle for the quadrant
#                 rect = fitz.Rect(
#                     positions[j][0],  # x1
#                     positions[j][1],  # y1
#                     positions[j][0] + a4_width / 2,  # x2
#                     positions[j][1] + a4_height / 2,  # y2
#                 )
#
#                 # Instead of generating a pixmap, use show_pdf_page to directly add the page
#                 new_page.show_pdf_page(rect, new_pdf, i + j)
#
#     return combined_pdf
# Create your views here.
@csrf_exempt
def cropper_main(request):
    if request.method == 'POST':
        pdf_file = request.FILES.getlist('pdf_file[]')
        printer_type = request.POST.get('printer_type')

        if pdf_file:
            new_list = list()
            for i in pdf_file:
                # Create a temporary file to save the uploaded PDF
                with tempfile.NamedTemporaryFile(delete=False) as temp_pdf_file:
                    # Write the contents of the uploaded file to the temporary file
                    for chunk in i.chunks():
                        temp_pdf_file.write(chunk)

                    # Now, open the temporary file using fitz
                    temp_pdf_file_path = temp_pdf_file.name
                    input_pdf = fitz.open(temp_pdf_file_path)

                    if len(input_pdf) > 1:
                        page = input_pdf[1]
                    else:
                        page = input_pdf[0]

                    # Search for boundary texts shiprocket
                    text_instances_shiprocket_1 = page.search_for("DELIVER TO:")
                    text_instances_shiprocket_2 = page.search_for(
                        "THIS IS AN AUTO-GENERATED LABEL AND DOES NOT NEED SIGNATURE.")

                    # Search for boundary texts flipkart
                    text_instances_flipkart_1 = page.search_for("E-Kart Logistics")
                    text_instances_flipkart_2 = page.search_for("AWB No.")

                    # Search for boundary texts amazon
                    text_instances_amazon_1 = page.search_for("Whether tax is payable under reverse charge")
                    text_instances_amazon_2 = page.search_for("Amazon Seller Services Pvt. Ltd.")

                    # Search for boundary texts meesho
                    text_instances_meesho_1 = page.search_for("Tax is not payable on reverse charge basis.")
                    text_instances_meesho_2 = page.search_for("If undelivered, return to:")

                    if text_instances_shiprocket_1 and text_instances_shiprocket_2:
                        pdf = shiprocket_converter(temp_pdf_file_path)
                    elif text_instances_flipkart_1 and text_instances_flipkart_2:
                        pdf = flipkart_converter(temp_pdf_file_path)
                    elif text_instances_meesho_1 and text_instances_meesho_2:
                        pdf = meesho_converter(temp_pdf_file_path)
                    elif text_instances_amazon_1 and text_instances_amazon_2:
                        pdf = amazon_converter(temp_pdf_file_path)
                    else:
                        json_data = {
                            'id': 0,
                            'msg': "Invalid PDF type. We only accept Shiprocket, Flipkart, Meesho, Amazon lable PDFs.",
                        }
                        return JsonResponse(json_data)
                    new_list.append(pdf)

            merge_pdf = merge_pdfs(new_list)
            cropped_pdf_bytes = BytesIO()

            if printer_type == "thermal_printer":
                if len(merge_pdf) > 0:
                    merge_pdf.save(cropped_pdf_bytes)
                else:
                    print("No pages with text found. Output PDF not created.")

            elif printer_type == "inkjet_printer":
                inject_pdf = inject_printer_common(merge_pdf)
                if len(inject_pdf) > 0:
                    inject_pdf.save(cropped_pdf_bytes)
                else:
                    print("No pages with text found. Output PDF not created.")

            cropped_pdf_bytes.seek(0)

            ts = time.strftime("%d%m%y-%H%M%S")
            file_name = 'SellerWise_' + ts + '.pdf'
            file_path = default_storage.save(file_name, ContentFile(cropped_pdf_bytes.read()))
            download_url = default_storage.url(file_path)
            print(download_url)

            return JsonResponse({'id': 1, 'msg':'PDF Submitted Successfully', 'download_url': download_url})

        else:
            json_data = {
                'id': 0,
                'msg': "No file uploaded!!! Please Upload a File."
            }
            return JsonResponse(json_data)

    return render(request, 'cropper_new.html')


def amazon_converter(pdf_file):
    try:
        input_pdf = fitz.open(pdf_file)

        # Create a new PDF to store the cropped pages
        cropped_pdf_bytes = BytesIO()
        new_pdf = fitz.open()

        # Extract odd-numbered pages (0-based indexing)
        for page_num in range(input_pdf.page_count):
            page = input_pdf[page_num]

            # Search for boundary texts meesho
            text_instances_amazon_1 = page.search_for("Whether tax is payable under reverse charge")
            text_instances_amazon_2 = page.search_for("Amazon Seller Services Pvt. Ltd.")

            if not (text_instances_amazon_1 and text_instances_amazon_2):
                new_pdf.insert_pdf(input_pdf, from_page=page_num, to_page=page_num)

        # Save the output PDF
        if len(new_pdf) > 0:
            new_pdf.save(cropped_pdf_bytes)
        else:
            print("No pages with text found. Output PDF not created.")

        return new_pdf


    except Exception as e:
        # Handle errors (e.g., invalid PDF file)
        return HttpResponse(f"An error occurred: {str(e)}", status=400)
# def amazon_converter(pdf_file):
#     try:
#         input_pdf = fitz.open(pdf_file)
#         cropped_pdf_bytes = BytesIO()
#         new_pdf = fitz.open()
#
#         # Thermal printer dimensions (4"x6" in points, 72ppi)
#         page_width = 288  # 4 inches * 72 points/inch
#         page_height = 432  # 6 inches * 72 points/inch
#
#         for page_num in range(input_pdf.page_count):
#             page = input_pdf[page_num]
#
#             # Check for Amazon-specific content
#             amazon_text1 = page.search_for("Whether tax is payable under reverse charge")
#             amazon_text2 = page.search_for("Amazon Seller Services Pvt. Ltd.")
#
#             if not (amazon_text1 and amazon_text2):
#                 # Create new page with thermal printer dimensions
#                 new_page = new_pdf.new_page(width=page_width, height=page_height)
#
#                 # Calculate scaling factors
#                 original_rect = page.rect
#                 scale_factor = min(page_width / original_rect.width,
#                                    page_height / original_rect.height)
#
#                 # Create transformation matrix
#                 matrix = fitz.Matrix(scale_factor, scale_factor)
#
#                 # Show original page content on new page with scaling
#                 new_page.show_pdf_page(
#                     new_page.rect,  # where to show (entire page)
#                     input_pdf,  # source PDF
#                     page_num,  # source page number
#                     transform=matrix,  # apply scaling
#                 )
#         if len(new_pdf) > 0:
#             new_pdf.save(cropped_pdf_bytes, garbage=4, deflate=True)
#         else:
#             print("No pages with text found. Output PDF not created.")
#
#         return new_pdf
#     except Exception as e:
#              # Handle errors (e.g., invalid PDF file)
#         return HttpResponse(f"An error occurred: {str(e)}", status=400)



def meesho_converter(pdf_file):
    try:
        input_pdf = fitz.open(pdf_file)
        cropped_pdf_bytes = BytesIO()
        new_pdf = fitz.open()

        # Thermal printer size in points (4x6 inches)
        THERMAL_WIDTH = 288  # 4 inches = 288 points
        THERMAL_HEIGHT = 429  # 6 inches = 432 points

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
            right = page.rect.width  # X-coordinate of the bottom-right corner (full width)
            bottom = text_instances_meesho_1[0][3] + 20  # Adjust as needed

            # Crop the page by creating a transformation matrix with DPI scaling
            cropped_page = page.get_pixmap(matrix=mat, clip=fitz.Rect(left, top, right, bottom))

            # Convert to grayscale to reduce size (optional)
            if cropped_page.n < 5:  # Check if the image is not already grayscale
                cropped_page = fitz.Pixmap(fitz.csGRAY, cropped_page)

            # Create a new page in the new PDF with thermal printer size (4x6 inches)
            new_page = new_pdf.new_page(width=THERMAL_WIDTH, height=THERMAL_HEIGHT)

            # Insert the cropped image into the thermal printer-sized page, resizing it to exactly fit
            new_page.insert_image(
                fitz.Rect(0, 0, THERMAL_WIDTH, THERMAL_HEIGHT),  # Fill the entire thermal printer page
                pixmap=cropped_page,
                keep_proportion=False  # Disable aspect ratio preservation
            )

        # Save the output PDF with optimization
        if len(new_pdf) > 0:
            new_pdf.save(cropped_pdf_bytes, garbage=4, deflate=True)
        else:
            print("No pages with text found. Output PDF not created.")

        return new_pdf

    except Exception as e:
        # Handle errors (e.g., invalid PDF file)
        return HttpResponse(f"An error occurred: {str(e)}", status=400)


def flipkart_converter(pdf_file):
    try:
        input_pdf = fitz.open(pdf_file)
        cropped_pdf_bytes = BytesIO()
        new_pdf = fitz.open()

        # A4 dimensions in points (595 x 842)
        A4_WIDTH = 288
        A4_HEIGHT = 429

        # Set a higher DPI for better quality (e.g., 300 DPI)
        zoom_x = 3.0  # Horizontal scaling factor based on DPI
        zoom_y = 3.0  # Vertical scaling factor based on DPI
        mat = fitz.Matrix(zoom_x, zoom_y)  # Create a transformation matrix for scaling

        # Iterate through all pages in the PDF
        for page_num in range(len(input_pdf)):
            page = input_pdf[page_num]

            # Search for boundary texts
            text_instances_flipkart_1 = page.search_for("E-Kart Logistics")
            text_instances_flipkart_3 = page.search_for("QTY")
            text_instances_flipkart_2 = page.search_for("Not for resale.")

            if not (text_instances_flipkart_1 and text_instances_flipkart_2):
                continue

            # Define the cropping box
            left = text_instances_flipkart_1[0].x0 - 30  # Left padding
            top = text_instances_flipkart_1[0].y0 - 10   # Top padding
            right = text_instances_flipkart_3[0].x1 + 8  # Right padding
            bottom = text_instances_flipkart_2[0].y1 + 11 # Bottom padding

            # Crop the page
            crop_rect = fitz.Rect(left, top, right, bottom)
            cropped_page = page.get_pixmap(matrix=mat, clip=crop_rect)

            # Calculate scaling to fit A4
            scale_x = A4_WIDTH / cropped_page.width
            scale_y = A4_HEIGHT / cropped_page.height
            scale = min(scale_x, scale_y)  # Maintain aspect ratio

            # Create a new A4 page
            new_page = new_pdf.new_page(width=A4_WIDTH, height=A4_HEIGHT)

            # Calculate the position to center the cropped content on the A4 page
            x_offset = (A4_WIDTH - (cropped_page.width * scale)) / 2
            y_offset = (A4_HEIGHT - (cropped_page.height * scale)) / 2

            # Insert the cropped and resized content into the A4 page
            new_page.insert_image(
                fitz.Rect(x_offset, y_offset, A4_WIDTH - x_offset, A4_HEIGHT - y_offset),
                pixmap=cropped_page,
            )

        # Save the output PDF with compression
        if len(new_pdf) > 0:
            new_pdf.save(cropped_pdf_bytes, deflate=True)  # Enable compression
        else:
            print("No pages with text found. Output PDF not created.")


        return new_pdf

    except Exception as e:
        # Handle errors (e.g., invalid PDF file)
        return HttpResponse(f"An error occurred: {str(e)}", status=400)


def shiprocket_converter(pdf_file, left_padding=10, right_padding=10):
    try:
        # Open the input PDF
        input_pdf = fitz.open(pdf_file)

        # Create a new PDF to store the cropped pages
        cropped_pdf_bytes = BytesIO()
        new_pdf = fitz.open()

        # A4 dimensions in points (1 point = 1/72 inch)
        A4_WIDTH = 595.28
        A4_HEIGHT = 841.89

        for page_number in range(len(input_pdf)):
            page = input_pdf[page_number]
            page_width, page_height = page.rect.width, page.rect.height

            # Search for boundary texts
            text_instances_deliver_to = page.search_for("DELIVER TO:")
            text_instances_label = page.search_for("THIS IS AN AUTO-GENERATED LABEL AND DOES NOT NEED SIGNATURE.")

            if not (text_instances_deliver_to and text_instances_label):
                continue

            deliver_to_top = text_instances_deliver_to[0].y0
            label_bottom = text_instances_label[0].y1 + 5

            # Get all text blocks on the page
            text_blocks = page.get_text("blocks")

            # Split text blocks into left and right sections
            mid_x = page_width / 2
            left_blocks = [block for block in text_blocks if block[0] < mid_x]
            right_blocks = [block for block in text_blocks if block[0] >= mid_x]

            # Find leftmost and rightmost coordinates for each section
            if left_blocks:
                left_crop_x = min(block[0] for block in left_blocks)
                left_crop_x = max(0, left_crop_x - left_padding)  # Apply left padding
            else:
                left_crop_x = 0

            if right_blocks:
                right_crop_x = max(block[2] for block in right_blocks)
                right_crop_x = min(right_crop_x + right_padding, page_width)  # Apply right padding
            else:
                right_crop_x = page_width

            # Define rectangles for left and right halves with all padding
            left_rect = fitz.Rect(
                left_crop_x,
                deliver_to_top,
                page_width / 2,
                label_bottom
            )

            right_rect = fitz.Rect(
                page_width / 2,
                deliver_to_top,
                right_crop_x,
                label_bottom
            )

            # Extract left half of the page
            left_page = fitz.open()
            left_page.new_page(
                width=page_width / 2 - left_crop_x,
                height=label_bottom - deliver_to_top
            )
            left_page[0].show_pdf_page(left_page[0].rect, input_pdf, page_number, clip=left_rect)

            # Extract right half of the page
            right_page = fitz.open()
            right_page.new_page(
                width=right_crop_x - page_width / 2,
                height=label_bottom - deliver_to_top
            )
            right_page[0].show_pdf_page(right_page[0].rect, input_pdf, page_number, clip=right_rect)

            # Resize and insert left half into A4 page
            if left_page[0].get_text():
                new_page = new_pdf.new_page(width=A4_WIDTH, height=A4_HEIGHT)
                new_page.show_pdf_page(
                    fitz.Rect(0, 0, A4_WIDTH, A4_HEIGHT),  # Fill the entire A4 page
                    left_page,  # Source PDF
                    0,  # Page number
                    clip=left_page[0].rect  # Use the entire left page
                )

            # Resize and insert right half into A4 page
            if right_page[0].get_text():
                new_page = new_pdf.new_page(width=A4_WIDTH, height=A4_HEIGHT)
                new_page.show_pdf_page(
                    fitz.Rect(0, 0, A4_WIDTH, A4_HEIGHT),  # Fill the entire A4 page
                    right_page,  # Source PDF
                    0,  # Page number
                    clip=right_page[0].rect  # Use the entire right page
                )

            # Close temporary PDFs
            left_page.close()
            right_page.close()

        # Save the output PDF
        if len(new_pdf) > 0:
            new_pdf.save(cropped_pdf_bytes)
        else:
            print("No pages with text found. Output PDF not created.")

        return new_pdf

    except Exception as e:
        # Handle errors (e.g., invalid PDF file)
        return HttpResponse(f"An error occurred: {str(e)}", status=400)


def inject_printer_common(new_pdf):
    # Create a new PDF to store the combined pages
    combined_pdf = fitz.open()

    # Define A4 page size in points (1 mm = 2.83465 points)
    a4_width = 593  # 210 mm
    a4_height = 840  # 297 mm

    # Define the positions for the 4 quadrants
    positions = [
        (0, 0),  # Top-left
        (a4_width / 2, 0),  # Top-right
        (0, a4_height / 2),  # Bottom-left
        (a4_width / 2, a4_height / 2),  # Bottom-right
    ]

    # Iterate through the new_pdf in chunks of 4 pages
    for i in range(0, len(new_pdf), 4):
        # Create a new A4 page in the output PDF
        new_page = combined_pdf.new_page(width=a4_width, height=a4_height)

        # Paste each of the 4 pages onto the new page
        for j in range(4):
            if i + j < len(new_pdf):
                page = new_pdf[i + j]

                # Define the target rectangle for the quadrant
                rect = fitz.Rect(
                    positions[j][0],  # x1
                    positions[j][1],  # y1
                    positions[j][0] + a4_width / 2,  # x2
                    positions[j][1] + a4_height / 2,  # y2
                )

                # Instead of generating a pixmap, use show_pdf_page to directly add the page
                new_page.show_pdf_page(rect, new_pdf, i + j)

    return combined_pdf


def merge_pdfs(pdf_list):
    # Create a new empty PDF to hold the merged result
    merged_pdf = fitz.open()

    # Iterate through the list of documents
    for doc in pdf_list:
        # Insert each document into the merged_pdf
        merged_pdf.insert_pdf(doc)

    # Save the merged document to a file
    merged_pdf.save("merged_output.pdf")

    return merged_pdf
