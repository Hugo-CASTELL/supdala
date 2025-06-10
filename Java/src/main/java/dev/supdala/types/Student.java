package dev.supdala.types;

import dev.supdala.types.preferences.Preferences;

public class Student {
    //#region Fields

    private Preferences<School> preferences;
    private String name;

    private School school;

    //#endregion Fields

    //#region Constructor

    public Student(String name) {
        this.name = name;

        this.school = null;
        this.preferences = new Preferences<>();
    }

    //#endregion Constructor

    //#region Getter and Setters

    public void addPreference(School school, int position) {
        this.preferences.put(school, position);
    }

    public String getName() {
        return this.name;
    }

    //#endregion Getter and Setters
}
