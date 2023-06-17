import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard:
    """显示得分信息的类"""

    def __init__(self, game_settings, screen, stats):
        """初始化显示得分涉及的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.game_settings = game_settings
        self.stats = stats

        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        # None表示使用默认字体，48表示字号
        self.font = pygame.font.SysFont(None, 48)

        # 准备初始得分图像
        self.prep_score()
        # 准备包含最高得分和当前得分的图像
        self.prep_high_score()
        # 准备包含等级的图像
        self.prep_level()
        # 准备包含余下飞船数的图像
        self.prep_ships()

    def prep_score(self):
        """将得分转换为一幅渲染的图像"""
        # 将得分圆整到最近的10的整数倍
        # round()函数通常让小数精确到小数点后指定的位数
        # 第二个实参-1指出圆整到最近的10、100、1000等整数倍
        rounded_score = round(self.stats.score, -1)
        # 将得分转换为字符串
        # 再将字符串传递给函数"{:,}".format()，它让Python将数值转换为字符串时在其中插入逗号
        score_str = "{:,}".format(rounded_score)
        # render()方法将存储在score_str中的文本转换为图像，然后将该图像存储在score_image中
        # 要将文本转换为图像，必须提供要渲染的文本以及指定文本颜色和背景色的信息
        # 通过将布尔实参True传递给render()，可让pygame根据字符串创建图像，还可指定字体和背景色
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.game_settings.bg_color
        )

        # 将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        # 将得分放在屏幕右上角，距离屏幕右边缘20像素，距离屏幕上边缘20像素
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """将最高得分转换为渲染的图像"""
        # 将最高得分圆整到最近的10的整数倍
        # round()函数通常让小数精确到小数点后指定的位数
        # 第二个实参-1指出圆整到最近的10、100、1000等整数倍
        high_score = round(self.stats.high_score, -1)
        # 将最高得分转换为字符串
        # 再将字符串传递给函数"{:,}".format()，它让Python将数值转换为字符串时在其中插入逗号
        high_score_str = "{:,}".format(high_score)
        # render()方法将存储在high_score_str中的文本转换为图像，然后将该图像存储在high_score_image中
        # 要将文本转换为图像，必须提供要渲染的文本以及指定文本颜色和背景色的信息
        # 通过将布尔实参True传递给render()，可让pygame根据字符串创建图像，还可指定字体和背景色
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, self.game_settings.bg_color
        )

        # 将最高得分放在屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        # 将最高得分放在屏幕顶部中央，距离屏幕上边缘20像素
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """将等级转换为渲染的图像"""
        # 将等级转换为字符串
        level_str = str(self.stats.level)
        # render()方法将存储在level_str中的文本转换为图像，然后将该图像存储在level_image中
        # 要将文本转换为图像，必须提供要渲染的文本以及指定文本颜色和背景色的信息
        # 通过将布尔实参True传递给render()，可让pygame根据字符串创建图像，还可指定字体和背景色
        self.level_image = self.font.render(
            level_str, True, self.text_color, self.game_settings.bg_color
        )

        # 将等级放在得分下方
        self.level_rect = self.level_image.get_rect()
        # 将等级放在得分下方，距离屏幕右边缘20像素，距离屏幕上边缘20像素
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """显示还余下多少艘飞船"""
        # 创建一个空编组，用于存储飞船实例
        self.ships = Group()
        # 创建飞船实例
        # 遍历编组ships中的飞船
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.game_settings, self.screen)
            # 设置飞船的位置
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            # 将飞船加入编组ships
            self.ships.add(ship)

    def show_score(self):
        """在屏幕上显示得分"""
        # 调用screen.blit()，并向它传递一幅图像以及与该图像相关联的rect对象，从而在屏幕上绘制文本图像
        self.screen.blit(self.score_image, self.score_rect)
        # 只要当前得分高于最高得分，就在屏幕上显示最高得分
        self.screen.blit(self.high_score_image, self.high_score_rect)
        # 调用screen.blit()，并向它传递一幅图像以及与该图像相关联的rect对象，从而在屏幕上绘制文本图像
        self.screen.blit(self.level_image, self.level_rect)
        # 在屏幕上绘制飞船
        # 遍历编组ships中的飞船实例，对每个飞船都调用draw()绘制到屏幕上
        self.ships.draw(self.screen)
