"""
The button module creates buttons to be placed on the screen
These buttons can have a sprite for when they are selected and unselected

As a sidenote, there was an odd issue with name caching for the buttons.
Even with unique names, they weren't able to be selected more than one time.
In order to fix this, I had to set the name of the buttons to a unique name 
every time they are selected (the limit for any number of clicks is the integer bit limit).
"""
from arcade import Sprite, Texture, load_texture
from PIL import Image, ImageFont, ImageDraw
from data import constants

global num_buttons
num_buttons = -1

class Button(Sprite):
    """
    The Button class is used to create buttons for the screen

    Methods:
        __init__(): initializes the parent class, assigns attributes
        coords_in_hitbox(): Returns a boolean based on if the given coords are inside the hitbox of the button
        select(): Sets the selected attribute to True and also sets the sprite to the corresponding selected sprite
        unselect(): Sets the selected attribute to False and also sets the sprite to the corresponding unselected sprite
    """
    def __init__(self, text="PLAY", text_color=(1, 93, 229), font=constants.DEFAULT_FONT, color="black", margin_width = 40, margin_height = 25, button_fill="black", outline="white", edge_thickness=5, font_size = 30, selectable=True, selected=False, selected_color=(12, 255, 255)):
        """
        initializes the parent class, assigns attributes

        Args:
            text (string): The text that will be displayed
            text_color (tuple|string): The color of the text displayed
            font (string): The font for the text
            color (tuple|string): The color of the background of the button (it is recommended that this be the color of the screen)
            margin_width (float): The space between the text and the sides of the button
            margin_height (float): The space between the text and the top and bottom of the button
            button_fill (tuple|string): The color for the inside portion of the button
            outline (tuple|string): The color for the edge of the button
            edge_thickness (float): The thickness of the edge
            font_size (int): The font size for the text
            selectable (bool): Sets whether or not the button is selectable
            selected (bool): Selects the button or not by default
            selected_color (tuple|string): Sets the color of the outline to this color when it is selected
        """

        super().__init__()
        self.append_texture(create_button(text=text, text_color=text_color, font=font, color=color, margin_width = margin_width, margin_height = margin_height, button_fill=button_fill, outline=outline, edge_thickness=edge_thickness, font_size = font_size))
        if selectable:
            self.append_texture(create_button(text=text, text_color=text_color, font=font, color=color, margin_width = margin_width, margin_height = margin_height, button_fill=button_fill, edge_thickness=edge_thickness, font_size = font_size, outline=selected_color))
        
        self.set_texture(0 if not selected else 1)
        
        self.selectable = selectable
        self.selected = selected
        self.new_name = True

    def coords_in_hitbox(self, x, y):
        """
        Returns a bool for if the coords given are inside the hitbox of the button

        Args:
            x (float): The x coordinate
            y (float): The y coordinate
        """
        return self.collides_with_point((x, y))

    def select(self):
        """
        Selects the button, changes the texture
        """
        if self.selectable:
            self.selected = True
            if self.texture == self.textures[0]:
                global num_buttons
                num_buttons += 1
                self.texture.name = num_buttons
                self.set_texture(1)
    
    def unselect(self):
        """
        Unselects the button, changes the texture
        """
        if self.selectable:
            self.selected = False
            if self.texture == self.textures[1]:
                global num_buttons
                num_buttons += 1
                self.texture.name = num_buttons
                self.set_texture(0)

def create_button(text="PLAY", text_color=(1, 93, 229), font=constants.DEFAULT_FONT, color="black", margin_width = 40, margin_height = 20, button_fill="black", outline="white", edge_thickness=10, font_size = 50):
    """
    Creates a button texture of type arcade.Texture

    Args:
        text (string): The text that will be displayed
        text_color (tuple|string): The color of the text displayed
        font (string): The font for the text
        color (tuple|string): The color of the background of the button (it is recommended that this be the color of the screen)
        margin_width (float): The space between the text and the sides of the button
        margin_height (float): The space between the text and the top and bottom of the button
        button_fill (tuple|string): The color for the inside portion of the button
        outline (tuple|string): The color for the edge of the button
        edge_thickness (float): The thickness of the edge
        font_size (int): The font size for the text
    """
    global num_buttons    
    font = ImageFont.truetype(font, size=font_size)

    # get text size
    text_size = font.getsize(text)

    # set button size + 10px margins
    button_size = (text_size[0] + margin_width, text_size[1] + margin_height)

    # create image with correct size and black background
    button_img = Image.new('RGBA', button_size, color)

    # put text on button with 10px margins
    button_draw = ImageDraw.Draw(button_img)
    width = button_size[0]
    height = button_size[1]
    button_draw.rounded_rectangle((0, 0, width, height), fill=button_fill, outline=outline, width=edge_thickness, radius=height/2)
    button_draw.text((margin_width / 2, margin_height / 2), text, font=font, fill=text_color)

    num_buttons += 1
    load_texture.texture_cache[num_buttons] = Texture(name=num_buttons, image=button_img)
    return load_texture.texture_cache[num_buttons]