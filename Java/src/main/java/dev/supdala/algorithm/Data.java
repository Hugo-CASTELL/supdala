package dev.supdala.algorithm;

import java.util.*;

import dev.supdala.types.School;
import dev.supdala.types.Student;
import org.apache.tools.ant.taskdefs.PathConvert;
import org.gradle.internal.impldep.com.amazonaws.transform.MapEntry;

public class Data {
    
    //#region Fields

    private RawJsonStructure rawJsonStructure;

    private Map<String, School> schools;
    private Map<String, Student> students;

    //#endregion Fields

    //#region Constructor

    public Data(RawJsonStructure raw) {
        this.rawJsonStructure = raw;

        this.schools = new HashMap<>();
        this.students = new HashMap<>();
    }

    //#endregion Constructor

    //#region Getters and setters

    public void addSchool(School school) {
        this.schools.put(school.getName(), school);
    }

    public void addStudent(Student student) {
        this.students.put(student.getName(), student);
    }

    public RawJsonStructure getRawJsonStructure() {
        return this.rawJsonStructure;
    }

    public School getSchool(String name) {
        return this.schools.get(name);
    }

    public Student getStudent(String name) {
        return this.students.get(name);
    }


    //#endregion Getters and setters
}
