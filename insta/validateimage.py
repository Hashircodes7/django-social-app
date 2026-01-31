from django.core.exceptions import ValidationError

def validate_image(file):
    max_size_mb = 5
    valid_formats = ['image/jpeg', 'image/png', 'image/gif']
    
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Image file too large (max {max_size_mb}MB)")
    if file.content_type not in valid_formats:
        raise ValidationError("Unsupported file type. Allowed: JPG, PNG, GIF")
