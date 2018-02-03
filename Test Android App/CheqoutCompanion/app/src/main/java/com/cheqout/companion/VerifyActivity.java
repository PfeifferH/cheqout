package com.cheqout.companion;

import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.QuerySnapshot;
import com.google.zxing.integration.android.IntentIntegrator;
import com.google.zxing.integration.android.IntentResult;

import java.util.ArrayList;
import java.util.List;

public class VerifyActivity extends AppCompatActivity {

    private static String TAG = "Verify";
    List<Transaction> myTrans;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_verify);

        IntentIntegrator integrator = new IntentIntegrator(VerifyActivity.this);
        integrator.initiateScan();

        myTrans = new ArrayList<>();
    }

    public void updateUI(){
        
    }

    public void onActivityResult(int requestCode, int resultCode, Intent intent) {
        IntentResult scanResult = IntentIntegrator.parseActivityResult(requestCode, resultCode, intent);
        if (scanResult != null) {
            // handle scan result
            Toast.makeText(VerifyActivity.this, scanResult.getContents(), Toast.LENGTH_LONG).show();
            FirebaseFirestore db = FirebaseFirestore.getInstance();
            db.collection("transaction")
                    .whereEqualTo("cart", scanResult.getContents())
                    .get()
                    .addOnCompleteListener(new OnCompleteListener<QuerySnapshot>() {
                        @Override
                        public void onComplete(@NonNull Task<QuerySnapshot> task) {
                            if (task.isSuccessful()) {
                                for (DocumentSnapshot document : task.getResult()) {
                                    Transaction trans = document.toObject(Transaction.class);
                                    myTrans.add(trans);
                                }
                                runOnUiThread(new Runnable() {
                                    @Override
                                    public void run() {
                                        updateUI();
                                    }
                                });
                            } else {
                                Log.e(TAG, "Error getting documents.", task.getException());
                            }
                        }
                    });

            // else continue with any other code you need in the method
        }
    }

}
