package com.cheqout.companion;

import android.content.Intent;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.CardView;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.EventListener;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.FirebaseFirestoreException;

import net.glxn.qrgen.android.QRCode;


public class LoyaltyActivity extends AppCompatActivity {

    private static String TAG = "Verify";
    private static String USER = "womvkAsNMvAIdKpnW2h3";

    ImageView ivLoyalty;
    TextView tvTitle;
    String loyaltyCode, name;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_loyalty);

        ivLoyalty = (ImageView) findViewById(R.id.ivLoyalty);
        tvTitle = (TextView) findViewById(R.id.tvTitle) ;

        CardView cvReceipt = (CardView) findViewById(R.id.cvReceipt);
        cvReceipt.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent myIntent = new Intent(LoyaltyActivity.this, VerifyActivity.class);
                myIntent.putExtra("user", USER); //Optional parameters
                CurrentActivity.this.startActivity(myIntent);

            }
        });

        FirebaseFirestore db = FirebaseFirestore.getInstance();
        final DocumentReference docRef = db.collection("users").document(USER);
        docRef.addSnapshotListener(new EventListener<DocumentSnapshot>() {
            @Override
            public void onEvent(@Nullable DocumentSnapshot snapshot,
                                @Nullable FirebaseFirestoreException e) {
                if (e != null) {
                    Log.w(TAG, "Listen failed.", e);
                    return;
                }

                if (snapshot != null && snapshot.exists()) {
                    Log.d(TAG, "Current data: " + snapshot.getData());
                    name = snapshot.getString("first");
                    loyaltyCode = snapshot.getString("loyalty");
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            Bitmap myBitmap = QRCode.from(loyaltyCode).withSize(250, 250).bitmap();
                            ivLoyalty.setImageBitmap(myBitmap);
                            tvTitle.setText("Welcome back " + name + ".");
                        }
                    });
                } else {
                    Log.d(TAG, "Current data: null");
                }
            }
        });
    }
}
