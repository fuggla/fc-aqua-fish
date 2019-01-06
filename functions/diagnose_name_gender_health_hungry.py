
import arcade

def diagnose_name_gender_health_hungry(fish_list):
    # Funtions som skriver ut fiskarnas status
    for fish in fish_list:
        arcade.draw_text(fish.name_gender[0] + " " + fish.name_gender[1] + " " + fish.attraction, fish.center_x, fish.center_y + 24,
                         arcade.color.BLACK, 18)
        arcade.draw_text(str(fish.health), fish.center_x, fish.center_y, arcade.color.BLACK, 18)
        arcade.draw_text(str(fish.hungry), fish.center_x, fish.center_y, arcade.color.BLACK, 18, anchor_x="left",
                         anchor_y="top")
