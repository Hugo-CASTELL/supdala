package dev.supdala.types.preferences;

import java.util.Dictionary;

public class Preferences<T> {

    //#region Fields

    private Dictionary<T, Integer> preferences;

    //#endregion Fields

    //#region Constructor

    public Preferences() {
        // Default constructor
    }

    //#endregion Constructor

    //#region Getters and Setters

    public Integer get(T key) {
        return preferences.get(key);
    }

    public void put(T key, Integer value) {
        this.preferences.put(key, value);
    }

    //#endregion Getters and Setters
}
