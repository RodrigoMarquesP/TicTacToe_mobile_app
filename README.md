# TicTacToe_mobile_app
A tictactoe mobile app developed with the minimax algorithm using  python and kivy

This algorihtm is a pratical implementation in kivy framework of the depth search minimax algorithm for optimal moves in a tictactoe game.  
The text will focus on the implementation, apk build and solutions to reach the ideal performance. To better comprehend minimax logics of the code, visit [the minimax project](https://github.com/RodrigoMarquesP/TicTacToe_minimax_depth_search).


### Implementing:
The best framework to develop mobile applications with python is kivy, which just the basics are necessary for this project, but fell free to learn more and implement it in different ways.  
The simple structure that was followed is to heriting a kivy.uix.widget.Widget class and configure its interface and components in a '.kv' file. At this specific project, inside the Widget object, i split the screen using GridLayout objects - which works similar to those from *matplotlib.pyplot* - and filling them with labels and buttons. The general configurations was just about colors, sizes, positions, paddings, font sizes and wich text appears, making the game screen looks like this:

<p align="center">
  <img src="images/game_screen.jpg" width="300">
</p>

<p align="center">
  <img src="images/game_screen2.jpeg" width="300">
</p>

