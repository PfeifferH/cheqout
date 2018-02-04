package com.cheqout.companion.Models;

import android.content.Context;
import android.content.res.TypedArray;
import android.support.v4.content.ContextCompat;
import android.support.v7.widget.CardView;
import android.text.TextUtils;
import android.util.AttributeSet;
import android.util.TypedValue;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.TextView;

import com.cheqout.companion.R;

/**
 * Created by angel on 2/3/2018.
 */

public class ReceiptCard extends CardView {

    private TextView mTitleView;
    private TextView mMessageView;
    private TextView mCardTypeView;
    private RelativeLayout mRLTypeView;
    public static final int ANIM_DURATION = 200;

    private View mRoot;

    public ReceiptCard(Context context) {
        super(context, null, 0);
        initialize(context, null, 0);
    }

    public ReceiptCard(Context context, AttributeSet attrs) {
        super(context, attrs, 0);
        initialize(context, attrs, 0);
    }

    public ReceiptCard(Context context, AttributeSet attrs, int defStyle) {
        super(context, attrs, defStyle);
        initialize(context, attrs, defStyle);
    }

    private void initialize(Context context, AttributeSet attrs, int defStyle) {
        LayoutInflater inflater = (LayoutInflater) context.getSystemService(
                Context.LAYOUT_INFLATER_SERVICE);
        mRoot = inflater.inflate(R.layout.card_receipt, this, true);
        mTitleView = (TextView) mRoot.findViewById(R.id.tvCardTitle);
        mMessageView = (TextView) mRoot.findViewById(R.id.tvCardInfo);
        mCardTypeView = (TextView) mRoot.findViewById(R.id.tvCardType);
        mRLTypeView = (RelativeLayout)   mRoot.findViewById(R.id.rlCardType);

        TypedArray a = context.obtainStyledAttributes(attrs, R.styleable.ReceiptCard, defStyle, 0);
        String title = a.getString(R.styleable.ReceiptCard_fc_title);
        setTitle(title);
        String text = a.getString(R.styleable.ReceiptCard_fc_title);
        setText(text);

        int dpValue = 16; // margin in dips
        float d = this.getResources().getDisplayMetrics().density;
        int margin = (int) (dpValue * d);

        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
        );

        params.setMargins(margin, 0, margin, margin);

        setLayoutParams(params);
        setRadius(getResources().getDimensionPixelSize(R.dimen.card_corner_radius));
        //setClickable(true);

        TypedValue outValue = new TypedValue();
        getContext().getTheme().resolveAttribute(android.R.attr.selectableItemBackground, outValue, true);

        setForeground(ContextCompat.getDrawable(context, outValue.resourceId));
        setCardElevation(getResources().getDimensionPixelSize(R.dimen.card_elevation));
        setPreventCornerOverlap(false);
    }


    /**
     * Use sparingly.
     */
    public void setTitle(String title) {
        if (TextUtils.isEmpty(title)) {
            mTitleView.setVisibility(View.GONE);
        } else {
            mTitleView.setVisibility(View.VISIBLE);
            mTitleView.setText(title);
        }
    }

    public void setText(String text) {
        if (TextUtils.isEmpty(text)) {
            mMessageView.setVisibility(View.GONE);
        } else {
            mMessageView.setVisibility(View.VISIBLE);
            mMessageView.setText(text);
        }
    }
    public void setType(int text) {
        if (text == 0) {
            mCardTypeView.setText("TRANSACTION RECEIPT");
            mRLTypeView.setBackgroundColor(ContextCompat.getColor(getContext(), R.color.colorAccent));
        } else {
            mCardTypeView.setText("UNPAID MERCHANDISE");
            mRLTypeView.setBackgroundColor(ContextCompat.getColor(getContext(), R.color.colorRed));
        }
    }
    public void dismiss() {
        dismiss(false);
    }

    public void dismiss(boolean animate) {
        if (!animate) {
            setVisibility(View.GONE);
        } else {
            animate().scaleY(0.1f).alpha(0.1f).setDuration(ANIM_DURATION);
        }
    }

    public void show() {
        setVisibility(View.VISIBLE);
    }
}
