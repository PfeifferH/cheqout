package com.cheqout.companion;

import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;

import com.cheqout.companion.Models.Item;
import com.cheqout.companion.Models.ReceiptCard;
import com.cheqout.companion.Models.Transaction;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.QuerySnapshot;
import com.google.zxing.integration.android.IntentIntegrator;
import com.google.zxing.integration.android.IntentResult;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class VerifyActivity extends AppCompatActivity {

    private static String TAG = "Verify";
    List<Transaction> myTrans;
    ReceiptCard tcUnpaid, tcOne, tcTwo, tcThree;
    FirebaseFirestore db;
    String unpaid = "";
    int numUnpaid, numUnpaidResolved;
    //TODO: Use a recycler view with cards

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_verify);

        db = FirebaseFirestore.getInstance();

        tcUnpaid = (ReceiptCard) findViewById(R.id.tcUnpaid);
        tcUnpaid.setType(1);
        tcOne = (ReceiptCard) findViewById(R.id.tcOne);
        tcTwo = (ReceiptCard) findViewById(R.id.tcTwo);
        tcThree = (ReceiptCard) findViewById(R.id.tcThree);

        myTrans = new ArrayList<>();
        Intent intent = getIntent();
        String userkey = intent.getStringExtra("user"); //if it's a string you stored.

        if (userkey == null || userkey.equals("")) {
            IntentIntegrator integrator = new IntentIntegrator(VerifyActivity.this);
            integrator.initiateScan();
        } else {
            getSupportActionBar().setTitle("Receipts");
            db.collection("transaction")
                    .whereEqualTo("user", userkey)
                    .get()
                    .addOnCompleteListener(new OnCompleteListener<QuerySnapshot>() {
                        @Override
                        public void onComplete(@NonNull Task<QuerySnapshot> task) {
                            if (task.isSuccessful()) {
                                for (DocumentSnapshot document : task.getResult()) {
                                    Log.e(TAG, "DocumentSnapshot data: " + document.getData().toString());
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
        }
    }

    public void updateUI() {
        if (myTrans != null && myTrans.size() != 0) {
            if (myTrans.size() >= 3) setTransaction(tcOne, myTrans.get(0));
            if (myTrans.size() >= 2) setTransaction(tcTwo, myTrans.get(1));
            if (myTrans.size() >= 1) setTransaction(tcOne, myTrans.get(0));
        }
    }

    public void setTransaction(ReceiptCard tc, Transaction trans) {
        tc.setVisibility(View.VISIBLE);
        if (trans.getItems() != null) {
            tc.setTitle("$" + String.format("%.02f", trans.getTotal()) + " received for " + trans.getItems().size() + " items");
            String receipt = trans.getTimestamp() + "\n\n************\n";
            for (HashMap<String, Object> obj : trans.getItems()) {
                Item myItem = new Item(obj);
                if (myItem.getQty() == 0 && myItem.getWeight() > 0) {
                    receipt = receipt + myItem.getName() + "    $" + String.format("%.02f", myItem.getUnit_price()) + " x " + String.format("%.02f", myItem.getWeight()) + " lb    $" + myItem.getUnit_price() * myItem.getWeight() + "\n";
                } else if (myItem.getQty() > 0 && myItem.getWeight() == 0) {
                    receipt = receipt + myItem.getName() + "    $" + String.format("%.02f", myItem.getUnit_price()) + " x " + myItem.getQty() + "    $" + String.format("%.02f", myItem.getUnit_price() * myItem.getQty()) + "\n";
                } else {
                    receipt = receipt + myItem.getName() + "    $" + String.format("%.02f", myItem.getUnit_price()) + "*0    $0.00\n";
                }
            }
            receipt = receipt + "************\n\nSubtotal: $" + String.format("%.02f", trans.getSubtotal()) + "\nTax: $" + String.format("%.02f", trans.getTax()) + "\nTotal: $" + String.format("%.02f", trans.getTotal());

            if (trans.getPayment_type() == 0) {
                receipt = receipt + "\n\nCASH";
            } else if (trans.getPayment_type() == 1) {
                receipt = receipt + "\n\nCREDIT/DEBIT\nAuth: " + trans.getAuth_code();
            }
            tc.setText(receipt);
        } else {
            tc.setTitle("VOID Transaction");
        }
    }

    private void addToUnpaid(long type, String name, double quantity) {
        if (type == 1) {
            unpaid = unpaid + name + " x " + (int) quantity + "\n";
        } else if (type == 2) {
            unpaid = unpaid + name + " x " + quantity + " lb\n";
        }
        numUnpaidResolved++;

        checkUnpaidComplete();
    }

    private void checkUnpaidComplete() {
        if (numUnpaid == numUnpaidResolved) {
            tcUnpaid.setText(unpaid);
            tcUnpaid.setVisibility(View.VISIBLE);
            tcUnpaid.setTitle(numUnpaid + " Unpaid Items");
        }
    }

    public void onActivityResult(int requestCode, int resultCode, Intent intent) {
        IntentResult scanResult = IntentIntegrator.parseActivityResult(requestCode, resultCode, intent);
        if (scanResult != null) {
            // handle scan result
            //Toast.makeText(VerifyActivity.this, scanResult.getContents(), Toast.LENGTH_LONG).show();
            Log.e("AHHH", "1");
            if (scanResult.getContents() != null) {
                Log.e("AHHH", "2");
                db.collection("carts").document(scanResult.getContents())
                        .get()
                        .addOnCompleteListener(new OnCompleteListener<DocumentSnapshot>() {
                            @Override
                            public void onComplete(@NonNull Task<DocumentSnapshot> task) {
                                Log.e("AHHH", "3");
                                if (task.isSuccessful()) {
                                    Log.e("AHHH", "4");
                                    final DocumentSnapshot cart = task.getResult();
                                    if (cart.getString("state") != null && cart.getString("state").equals("active")) {
                                        Log.e("AHHH", "5");
                                        final List<HashMap<String, Object>> items = (List) cart.get("items");
                                        numUnpaid = items.size();
                                        numUnpaidResolved = 0;
                                        unpaid = "";
                                        for (HashMap<String, Object> item : items) {
                                            final HashMap<String, Object> myItem = item;
                                            db.collection("inventory").document(item.get("id").toString()).get().addOnCompleteListener(new OnCompleteListener<DocumentSnapshot>() {
                                                @Override
                                                public void onComplete(@NonNull Task<DocumentSnapshot> task) {
                                                    final DocumentSnapshot results = task.getResult();
                                                    if (results.exists()) {
                                                        runOnUiThread(new Runnable() {
                                                            @Override
                                                            public void run() {
                                                                addToUnpaid((results.getLong("type")), results.getString("name"), Double.parseDouble(myItem.get("quantity").toString()));
                                                            }
                                                        });
                                                    } else {
                                                        numUnpaid--;
                                                        runOnUiThread(new Runnable() {
                                                            @Override
                                                            public void run() {
                                                                checkUnpaidComplete();
                                                            }
                                                        });
                                                    }
                                                }
                                            });
                                        }
                                    }

                                }
                            }
                        });
                Log.e("AHHH", "7");
                db.collection("transaction")
                        .whereEqualTo("cart", scanResult.getContents())
                        .limit(3)
                        .get()
                        .addOnCompleteListener(new OnCompleteListener<QuerySnapshot>() {
                            @Override
                            public void onComplete(@NonNull Task<QuerySnapshot> task) {
                                Log.e("AHHH", "8");
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
            } else {
                Log.e("AHHH", "9");
                VerifyActivity.this.finish();
            }
        } else {
            Log.e("AHHH", "10");
            VerifyActivity.this.finish();
        }
    }

}
