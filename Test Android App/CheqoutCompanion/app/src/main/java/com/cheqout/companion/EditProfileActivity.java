package com.cheqout.companion;

import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Switch;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.SetOptions;

import java.util.HashMap;
import java.util.Map;

public class EditProfileActivity extends AppCompatActivity {

    FirebaseFirestore db;
    String userkey;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_edit_profile);

        final EditText etFName = (EditText) findViewById(R.id.etFName);
        final EditText etLName = (EditText) findViewById(R.id.etLName);
        final EditText etEmail = (EditText) findViewById(R.id.etEmail);
        final EditText etMobile = (EditText) findViewById(R.id.etMobile);
        final Switch swSMS = (Switch) findViewById(R.id.swSMS);
        final Button bSave = (Button) findViewById(R.id.bSave);

        Intent intent = getIntent();
        userkey = intent.getStringExtra("user"); //if it's a string you stored.

        db = FirebaseFirestore.getInstance();
        if (userkey == null || userkey.equals("")) {
            finish();
        } else {
            db.collection("users").document(userkey).get().addOnCompleteListener(new OnCompleteListener<DocumentSnapshot>() {
                @Override
                public void onComplete(@NonNull Task<DocumentSnapshot> task) {
                    DocumentSnapshot user = task.getResult();
                    if (user.exists()) {
                        if (user.getString("first") != null)
                            etFName.setText(user.getString("first"));
                        if (user.getString("last") != null) etLName.setText(user.getString("last"));
                        if (user.getString("email") != null)
                            etEmail.setText(user.getString("email"));
                        if (user.getString("mobile") != null)
                            etMobile.setText(user.getString("mobile"));
                        if (user.getBoolean("sms") != null)
                            swSMS.setChecked(user.getBoolean("sms"));
                    } else {
                        finish();
                    }
                }
            });
        }

        bSave.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Map<String, Object> user = new HashMap<>();
                user.put("first", etFName.getText().toString());
                user.put("last", etLName.getText().toString());
                user.put("email", etEmail.getText().toString());
                user.put("mobile", etMobile.getText().toString());
                user.put("sms", swSMS.isChecked());

                db.collection("users").document(userkey)
                        .set(user, SetOptions.merge())
                        .addOnSuccessListener(new OnSuccessListener<Void>() {
                            @Override
                            public void onSuccess(Void aVoid) {
                                Toast.makeText(EditProfileActivity.this, "Changes saved", Toast.LENGTH_SHORT).show();
                                finish();
                            }
                        })
                        .addOnFailureListener(new OnFailureListener() {
                            @Override
                            public void onFailure(@NonNull Exception e) {
                                Toast.makeText(EditProfileActivity.this, "Changes could not be saved", Toast.LENGTH_SHORT).show();
                            }
                        });
            }
        });
    }
}