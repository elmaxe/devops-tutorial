package main.java.demo;

public class Year {

    private int year;

    public Year(int year) {
        this.year = year;
    }

    public String review() {
        switch (year) {
        case 0:
            return "Jesus Christ what a year...";
        case 42:
            return "A year worth living for";
        case 1337:
            return ":sunglasses:";
        case 1984:
            return "You never felt alone";
        case 1987:
            return "https://www.youtube.com/watch?v=dQw4w9WgXcQ";
        case 2020:
            return "Sad year :(";
        default:
            return "Meh";
        }
    }
}
