package dev.supdala.algorithm;

import dev.supdala.types.School;
import dev.supdala.types.Student;
import org.gradle.internal.impldep.com.google.gson.Gson;

import java.io.FileReader;
import java.util.logging.Level;
import java.util.logging.Logger;

public final class StableMarriage {

    public Data extractDataFromJson(String jsonFilePath) {
        try {
            // Open JSON
            FileReader fileReader = new FileReader(jsonFilePath);
            RawJsonStructure raw = new Gson().fromJson(fileReader, RawJsonStructure.class);

            // Data holder
            Data data = new Data(raw);

            // Create students
            for(String studentName : raw.students.keySet()) {
                data.addStudent(new Student(studentName));
            }

            // Create schools
            for (String schoolName : raw.schools.keySet()) {
                int capacity = raw.capacity.get(schoolName);
                data.addSchool(new School(schoolName, capacity));
            }

            // Return read data
            return data;

        } catch (Exception e) {
            Logger.getLogger(this.getClass().getName()).log(Level.SEVERE, "Error while extracting data from json file", e);
            return null;
        }
    }

    public Data preProcess(Data data) {
        for (var entry : data.getRawJsonStructure().schools.entrySet()) {
            School school = data.getSchool(entry.getKey());

            int index = 1;
            for(String studentName : entry.getValue()){
                school.addPreference(data.getStudent(studentName), index);
                index++;
            }
        }

        for (var entry : data.getRawJsonStructure().students.entrySet()) {
            Student student = data.getStudent(entry.getKey());

            int index = 1;
            for(String schoolName : entry.getValue()){
                student.addPreference(data.getSchool(schoolName), index);
                index++;
            }
        }

        return data;
    }
}
