from stegano import lsb

# ===================================
# LARGE PAYLOAD
# ===================================

secret = "HiddenPayload" * 200

# ===================================
# INPUT / OUTPUT
# ===================================

input_image = "samples/clean_image.png"

output_image = "samples/stego_image.png"

# ===================================
# HIDE DATA
# ===================================

secret_image = lsb.hide(
    input_image,
    secret
)

secret_image.save(output_image)

print("✅ Stego image created:")
print(output_image)