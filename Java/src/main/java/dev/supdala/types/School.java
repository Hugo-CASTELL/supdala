package dev.supdala.types;

import dev.supdala.types.preferences.Preferences;
import org.gradle.internal.impldep.it.unimi.dsi.fastutil.Pair;

import java.util.ArrayList;
import java.util.List;

public class School {

    //#region Fields

    private Preferences<Student> preferences;
    private String name;
    private int capacityMax;

    private List<Student> students;
    private Pair<Student, Integer> leastPreferredStudent;

    //#endregion Fields

    //#region Constructor

    public School(String name, int capacityMax) {
        this.name = name;
        this.capacityMax = capacityMax;

        this.students = new ArrayList<>(capacityMax);
        this.preferences = new Preferences<>();
    }

    //#endregion Constructor

    //#region Getter and Setters

    public void addPreference(Student student, int position) {
        this.preferences.put(student, position);
    }

    public String getName() {
        return this.name;
    }

    public void addStudent(Student student) {
        this.students.add(student);

        int positionInPreferences = this.preferences.get(student);
        if(positionInPreferences < leastPreferredStudent.right()){
            leastPreferredStudent = Pair.of(student, positionInPreferences);
        }
    }

    public void isMore

    //#endregion Getter and Setters


}