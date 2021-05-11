package msdemo.ayhan.com.ecommerce;

import android.app.Activity;
import android.content.Context;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.support.design.widget.Snackbar;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;

import android.widget.TextView;


import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import java.util.ArrayList;

public class MedicationsAdapter extends ArrayAdapter<MedicationModel> {

    private ArrayList<MedicationModel> dataSet;
    Context mContext;
    View mView;

    // 1
    public MedicationsAdapter(ArrayList<MedicationModel> data, Context context, View view) {
        super(context, R.layout.listview_medications_row, data);
        this.dataSet = data;
        this.mContext=context;
        this.mView = view;

    }

    @Override
    public int getCount() {
        return dataSet.size();
    }

    @Override
    public long getItemId(int position) {
        return dataSet.get(position).getID();
    }

    @Override
    public MedicationModel getItem(int position) {
        return dataSet.get(position);
    }


    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        LayoutInflater inflater = (LayoutInflater) mContext
                .getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        View rowView = inflater.inflate(R.layout.listview_medications_row, parent, false);
        TextView txt_medication_name = rowView.findViewById(R.id.txt_medication_name);
        TextView txt_medication_price = rowView.findViewById(R.id.txt_medication_price);
        Button btn_medication_price = rowView.findViewById(R.id.txt_medication_buy);

        MedicationModel item = dataSet.get(position);
        txt_medication_name.setText(item.getName());
        txt_medication_price.setText(Float.toString(item.getPrice()));

        btn_medication_price.setOnClickListener((View v) -> {
            //LinearLayout vwParentRow = (LinearLayout)v.getParent();
            //TextView child = (TextView)vwParentRow.getChildAt(0);
            PlaceOrder(dataSet.get(position));

        });
        return rowView;
    }
    private void PlaceOrder(MedicationModel medication_item) {
        try {
            //json={"MedicationId":id, "MedicationName":name, "PatientId":session['username'], "TimeStamp":time.strftime("%Y-%d-%m %H:%M:%S", time.localtime())})
            SharedPreferences sharedPref = ((Activity)mContext).getPreferences(Context.MODE_PRIVATE);
            String user_name = sharedPref.getString(mContext.getString(R.string.saved_login_name), null);
            if (user_name == null) {
                Snackbar.make(mView, "Login first", Snackbar.LENGTH_LONG)
                        .setAction("No action", null).show();
                return;
            }
            java.util.Calendar calendar = java.util.Calendar.getInstance();
            java.text.SimpleDateFormat df = new java.text.SimpleDateFormat("yyyy-dd-MM hh:mm:ss");
            String formated_date = df.format(calendar.getTime());


            JsonObject post_json = new JsonObject();
            post_json.addProperty("MedicationId", medication_item.Code);
            post_json.addProperty("MedicationName", medication_item.Name);
            post_json.addProperty("PatientId", user_name);
            post_json.addProperty("TimeStamp", formated_date);


            String [] params = {"order/place-order/", "POST", post_json.toString()};


            new RestClientTask() {
                protected void onPostExecute(String result) {

                    JsonObject response_json = new JsonParser().parse(result).getAsJsonObject();
                    String result_string = response_json.get("Result").toString().replaceAll("\"", "");
                    if (result_string.equals("Success")) {
                        String data_string = response_json.get("Data").toString();
                        JsonObject data_json = new JsonParser().parse(data_string).getAsJsonObject();
                        String order_status = data_json.get("result").toString().replaceAll("\"", "");;
                        if (order_status.equals("Success")) {
                            //Do nothing
                            Snackbar.make(mView, "Order Placed. Checking credit and stocks. Check My Orders to watch status", Snackbar.LENGTH_LONG)
                                    .setAction("No action", null).show();
                        }
                        else {
                            Snackbar.make(mView, "Order Place Fail: " + order_status, Snackbar.LENGTH_LONG)
                                    .setAction("No action", null).show();
                        }


                    }
                    else {
                        Snackbar.make(mView, "Order Fail " + result, Snackbar.LENGTH_LONG)
                                .setAction("No action", null).show();
                    }

                }
            }.execute(params);
        }
        catch (Exception ex) {

        }
    }

}