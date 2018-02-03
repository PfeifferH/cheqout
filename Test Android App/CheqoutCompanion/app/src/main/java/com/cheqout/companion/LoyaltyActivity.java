package com.cheqout.companion;

import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.QuerySnapshot;

public class LoyaltyActivity extends AppCompatActivity {

    private static String TAG = "Verify";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_loyalty);

        FirebaseFirestore db = FirebaseFirestore.getInstance();
        db.collection("womvkAsNMvAIdKpnW2h3")
                .get()
                .addOnCompleteListener(new OnCompleteListener<QuerySnapshot>() {
                    @Override
                    public void onComplete(@NonNull Task<QuerySnapshot> task) {
                        if (task.isSuccessful() && task.getResult().getDocuments().get(0) != null) {
                            DocumentSnapshot user = task.getResult().getDocuments().get(0);
                            Log.e(TAG, "DocumentSnapshot data: " + user.getData().toString());
                            
                        } else {
                            Log.e(TAG, "Error getting documents.", task.getException());
                        }
                    }
                });

    }
}
