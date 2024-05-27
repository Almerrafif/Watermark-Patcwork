import cv2
import numpy as np

def apply_watermark_patchwork(original_path, watermark_path, output_path, alpha=0.1):
    # Membaca gambar asli dan watermark dalam format grayscale
    image = cv2.imread(original_path, cv2.IMREAD_GRAYSCALE)
    watermark = cv2.imread(watermark_path, cv2.IMREAD_GRAYSCALE)
    
    # Ubah ukuran watermark agar sesuai dengan gambar asli
    watermark = cv2.resize(watermark, (image.shape[1], image.shape[0]))
    
    # Buat salinan dari gambar asli untuk disisipi watermark
    watermarked_image = image.astype(np.float32)
    watermark = watermark.astype(np.float32)
    
    # Normalisasi watermark agar memiliki rentang nilai yang lebih sesuai
    watermark = watermark / 255.0
    
    # Sisipkan watermark dengan menambahkan alpha * watermark ke gambar asli
    watermarked_image += alpha * watermark * 255.0
    
    # Normalisasi hasil agar berada dalam rentang 0-255
    watermarked_image = np.clip(watermarked_image, 0, 255)
    
    # Konversi hasil ke tipe uint8
    watermarked_image = watermarked_image.astype(np.uint8)
    
    # Menyimpan gambar yang telah disisipi watermark
    cv2.imwrite(output_path, watermarked_image)

def extract_watermark_patchwork(watermarked_path, original_path, output_path, alpha=1):
    # Membaca gambar asli dan gambar yang diwatermark dalam format grayscale
    original = cv2.imread(original_path, cv2.IMREAD_GRAYSCALE)
    watermarked_image = cv2.imread(watermarked_path, cv2.IMREAD_GRAYSCALE)
    
    # Konversi gambar ke tipe float32 untuk perhitungan
    original = original.astype(np.float32)
    watermarked_image = watermarked_image.astype(np.float32)
    
    # Ekstraksi watermark dengan menghitung perbedaan antara gambar yang diwatermark dan gambar asli
    extracted_watermark = (watermarked_image - original) / alpha
    
    # Normalisasi hasil ekstraksi agar berada dalam rentang 0-255
    extracted_watermark = cv2.normalize(extracted_watermark, None, 0, 255, cv2.NORM_MINMAX)
    
    # Konversi ke tipe uint8
    extracted_watermark = extracted_watermark.astype(np.uint8)
    
    # Menyimpan watermark yang diekstrak
    cv2.imwrite(output_path, extracted_watermark)