# TicTacToe_mobile_app
A tictactoe mobile app developed with the minimax algorithm using  python and kivy

This algorihtm is a pratical implementation in kivy framework of the depth search minimax algorithm for optimal moves in a tictactoe game. The text will focus on the implementation, solutions to reach the ideal performance and the apk build. To better comprehend minimax logics of the code, visit [the minimax project](https://github.com/RodrigoMarquesP/TicTacToe_minimax_depth_search).


### Implementing:
The best framework to develop mobile applications with python is kivy, which just the basics are necessary for this project, but fell free to learn more and implement it in different ways.  
The simple structure that was followed is to heriting a kivy.uix.widget.Widget class and configure its interface and components in a '.kv' file. At this specific project, inside the Widget object, i split the screen using GridLayout objects - which works similar to those from *matplotlib.pyplot* - and filling them with labels and buttons. The general configurations was just about colors, sizes, positions, paddings, font sizes and wich text appears, making the game screen looks like this:
  

<p align="center">
  <img src="images/game_screen.jpg" width="300">
</p>

  
<p align="center">
  <img src="images/game_screen2.jpeg" width="300">
</p>

  
The basic of the main.py code is:

````
class MainGrid(Widget):
    # game machanics


class MyApp(App):
    def build(self):
        game = MainGrid()
        return game


if __name__ == "__main__":
    MyApp().run()
````


### Performance:

As discussed in [the minimax project](https://github.com/RodrigoMarquesP/TicTacToe_minimax_depth_search), the search goes along almost six hundred thousand nodes when exploring all states, what haves a high time cost, and the problem is solved just when there's already two marks on the tictactoe board - the search of the 7 left squares took less than one second in my computer. Considering that the mobile's resources are smaller than the computer's, we won't have a good performance at a 9 or 8 depth search.  

The solution that i came up with, was a trick already used in a lot of AI game agents to deal with the first moves - humans can't deal with deep searchs, but they know by experiencing, which are the better moves at the begginning of the game, so, they don't even have to think about. This way, if the agent knows what to do in the first two moves, it won't need to use the long search, but how to know be best two moves? We can just execute the minimax code to consult the utility of the states in each different possibility, and organize this knowledge for the easy acces of the agent.




