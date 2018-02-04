package com.cheqout.companion;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.google.firebase.firestore.FirebaseFirestore;

public class AddPaymentActivity extends AppCompatActivity {

    FirebaseFirestore db;
    String userkey;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_payment);

        final EditText etCard = (EditText) findViewById(R.id.etCard);
        final EditText etExpMonth = (EditText) findViewById(R.id.etExpMonth);
        final EditText etExpYear = (EditText) findViewById(R.id.etExpYear);
        final EditText etCVC = (EditText) findViewById(R.id.etCVC);
        final EditText etName = (EditText) findViewById(R.id.etName);
        final EditText etEmail = (EditText) findViewById(R.id.etEmail);
        final EditText etAddress = (EditText) findViewById(R.id.etAddress);
        final EditText etCity = (EditText) findViewById(R.id.etCity);
        final EditText etState = (EditText) findViewById(R.id.etState);
        final EditText etZIP = (EditText) findViewById(R.id.etZIP);

        final Button bSave = (Button) findViewById(R.id.bSave);

        Intent intent = getIntent();
        userkey = intent.getStringExtra("user");

        bSave.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(etCard.getText().toString().equals("") || etExpMonth.getText().toString().equals("") ||etExpYear.getText().toString().equals("") ||etCVC.getText().toString().equals("") ||etName.getText().toString().equals("") ||etEmail.getText().toString().equals("") ||etAddress.getText().toString().equals("") ||etCity.getText().toString().equals("") ||etState.getText().toString().equals("") ||etZIP.getText().toString().equals("")){
                    Toast.makeText(AddPaymentActivity.this, "Please fill in all the fields", Toast.LENGTH_SHORT).show();
                }else{

                }
            }
        });

    }
}
