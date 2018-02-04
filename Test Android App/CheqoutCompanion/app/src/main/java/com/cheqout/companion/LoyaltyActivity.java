package com.cheqout.companion;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.CardView;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.TextView;

import com.cheqout.companion.Fingerprint.FingerprintActivity;
import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.EventListener;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.FirebaseFirestoreException;


import net.glxn.qrgen.android.QRCode;


public class LoyaltyActivity extends AppCompatActivity {

    private static String TAG = "Verify";
    private static String USER = "womvkAsNMvAIdKpnW2h3";

    ImageView ivLoyalty,ivMinimize;
    TextView tvTitle;
    String loyaltyCode, name;
    LinearLayout llPayment;
    RelativeLayout rlShowHide;
    TextView tvPayment;

    boolean barcodeDisplayed = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_loyalty);

        ivLoyalty = (ImageView) findViewById(R.id.ivLoyalty);
        ivMinimize= (ImageView) findViewById(R.id.ivMinimize);
        tvTitle = (TextView) findViewById(R.id.tvTitle) ;

        llPayment = (LinearLayout) findViewById(R.id.llPayment);
        rlShowHide = (RelativeLayout) findViewById(R.id.rlShowHide);
        tvPayment = (TextView) findViewById(R.id.tvPayment);

        rlShowHide.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(barcodeDisplayed){
                    llPayment.setVisibility(View.GONE);
                    tvPayment.setText("Show Payment Barcode");
                    ivMinimize.setImageDrawable(getDrawable(R.drawable.ic_expand_more));
                    barcodeDisplayed = !barcodeDisplayed;
                }else{
                    Intent myIntent = new Intent(LoyaltyActivity.this, FingerprintActivity.class);
                    startActivityForResult(myIntent, 1);

                }

            }
        });

        CardView cvReceipt = (CardView) findViewById(R.id.cvReceipt);
        cvReceipt.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent myIntent = new Intent(LoyaltyActivity.this, VerifyActivity.class);
                myIntent.putExtra("user", USER); //Optional parameters
                LoyaltyActivity.this.startActivity(myIntent);

            }
        });

        CardView cvProfile = (CardView) findViewById(R.id.cvProfile);
        cvProfile.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {


            }
        });

        CardView cvEditPayment = (CardView) findViewById(R.id.cvEditPayment);
        cvEditPayment.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent myIntent = new Intent(LoyaltyActivity.this, PaymentActivity.class);
                myIntent.putExtra("user", USER); //Optional parameters
                LoyaltyActivity.this.startActivity(myIntent);
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

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {

        if (requestCode == 1) {
            if(resultCode == Activity.RESULT_OK){
                llPayment.setVisibility(View.VISIBLE);
                tvPayment.setText("Hide Payment Barcode");
                ivMinimize.setImageDrawable(getDrawable(R.drawable.ic_expand_less));
                barcodeDisplayed = !barcodeDisplayed;
            }
            if (resultCode == Activity.RESULT_CANCELED) {
                //Write your code if there's no result
            }
        }
    }
}
