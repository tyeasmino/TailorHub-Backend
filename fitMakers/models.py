from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=80)

    def __str__(self):
        return self.name
    

class FitMaker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # shop name 
    image = models.URLField(max_length=255, blank=True, null=True)

    # company details
    shop_started = models.DateField(blank=True, null=True) 
    shop_address = models.CharField(max_length=200, blank=True, null=True)
    shop_hours = models.CharField(max_length=100, blank=True, null=True)

    # contact details 
    phone = models.CharField(max_length=11, null=True, blank=True) 
    whatsapp = models.CharField(max_length=11, null=True, blank=True) 
    website = models.URLField(max_length=100, blank=True, null=True) 
    facebook = models.URLField(max_length=255, blank=True, null=True)
    instagram = models.URLField(max_length=255, blank=True, null=True)

    services = models.ManyToManyField(Service, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.shop_address if self.shop_address else ''}"







# 1. Saree
# The saree is a timeless symbol of grace and tradition, commonly worn in Bangladesh for weddings, religious ceremonies, and cultural festivals. Made from various fabrics like silk, cotton, or chiffon, the saree typically consists of a long piece of cloth (5-9 yards) draped around the body. With intricate embroidery, zari work, or contemporary designs, sarees are perfect for special occasions. The saree is versatile—whether it's a traditional look for a wedding or a simple design for a formal gathering, this garment has maintained its cultural significance for centuries. Available in a variety of colors, styles, and patterns, sarees can be accessorized with bangles, earrings, and the iconic bindi for a complete look.

# 2. Salwar Kameez
# Salwar Kameez is a staple in every Bangladeshi woman's wardrobe. Consisting of a long tunic (kameez), loose-fitting trousers (salwar), and a scarf or shawl (dupatta), this outfit combines comfort and style. It is worn for both formal and casual events, from office settings to family gatherings and religious functions. The salwar kameez offers an array of choices, including simple cotton versions for daily wear and intricate designs for weddings or festivals. The elegance and ease of movement make it a popular choice for women across generations.

# 3. Three-Piece Set (Salwar Kameez Set)
# The Three-Piece Set in Bangladesh typically refers to an ensemble that includes a salwar kameez with an added layer such as a jacket, vest, or cardigan. This modern take on the traditional salwar kameez brings a more stylish and layered look, making it perfect for semi-formal occasions, office wear, or evening gatherings. Often crafted in fabrics like cotton, georgette, or silk, these sets are designed with contemporary cuts and embellishments. The three-piece set adds sophistication while maintaining the comfort that comes with the salwar kameez.

# 4. Gown
# Western-style gowns have found their place in the evolving fashion landscape of Bangladesh. Gowns are commonly worn for weddings, formal parties, gala dinners, or any high-end event. These dresses range from flowing A-line gowns to form-fitting evening wear with delicate details like lace, sequins, or beading. Gowns are ideal for those who want a more glamorous, international look while still maintaining cultural elegance in their choice of accessories and fabrics. Whether opting for a traditional ball gown or a more modern cocktail dress, the gown offers an opportunity to stand out and make a statement.

# 5. Maxi Dress
# Maxi dresses are perfect for relaxed, yet stylish outfits. Popular for casual occasions like day trips, summer outings, or even dinner parties, these dresses typically feature a long, flowing design, often made from breathable fabrics like cotton, linen, or jersey. Available in a wide range of colors, prints, and cuts, maxi dresses offer versatility and comfort. They can be dressed up with accessories or worn casually, making them a go-to choice for women seeking an effortless yet fashionable look. Maxi dresses are particularly ideal for the warm weather of Bangladesh, offering style and comfort in equal measure.

# 6. Kurti
# The kurti is a stylish and practical piece of clothing that has become a favorite in urban and rural Bangladesh alike. Shorter than a traditional kameez, the kurti is typically worn with leggings, churidars, or jeans, making it an adaptable option for both casual and semi-formal events. Kurtis are available in various lengths and styles—from simple cotton designs for daily wear to more embellished versions for festive occasions. The versatility of kurtis makes them an essential part of the modern Bangladeshi woman's wardrobe. Whether paired with accessories or worn as-is, kurtis embody simplicity, elegance, and ease.

# 7. Shalwar
# Shalwar, the traditional loose trousers, are an essential part of many outfits in Bangladesh, often worn with a kameez or kurti. The relaxed fit of the salwar ensures comfort and flexibility, which is particularly appealing in the hot and humid climate of Bangladesh. While the classic salwar has a wide leg, the more contemporary styles include tapered or pleated versions that add modern flair. Salwars are often paired with dupattas to create a complete traditional look, suitable for daily wear, casual events, and even religious ceremonies. They are available in a variety of fabrics, making them perfect for every season.

# 8. Churidar
# The churidar is a more form-fitting version of the traditional salwar, featuring long, narrow legs that gather at the ankle. Often paired with a kameez or a kurti, the churidar creates a sleek, elegant silhouette. This style is perfect for more formal occasions or when a more contemporary look is desired. Churidars are highly popular for weddings, cultural events, or even day-to-day wear in urban settings. Available in many fabrics and colors, churidars add a refined touch to any outfit while providing ultimate comfort.

# 9. Dhoti Gown
# The dhoti gown is a modern fusion of traditional Bengali wear and contemporary fashion. Inspired by the classic dhoti, this gown merges cultural heritage with a chic, fashionable twist. The dhoti gown typically features a flowing lower half like a traditional gown, paired with a draped fabric similar to the dhoti. Often seen at upscale events, weddings, and formal parties, this unique garment allows women to embrace the essence of traditional Bangladeshi attire while enjoying the modern comfort of a gown. A perfect choice for those seeking to blend cultural identity with global fashion trends.

# 10. Peplum Top & Skirt
# Peplum tops paired with skirts are a modern addition to the Bangladeshi fashion scene, combining traditional elegance with contemporary design. Peplum tops, characterized by a short, flared section at the waist, create an hourglass figure and add structure to an outfit. When paired with a well-tailored skirt, this combination is perfect for both formal and semi-formal occasions, such as office events, cocktail parties, and evening gatherings. Peplum tops are available in many styles, including embroidered designs, making them suitable for various occasions, while skirts can range from pencil to flared, allowing for versatility in styling.