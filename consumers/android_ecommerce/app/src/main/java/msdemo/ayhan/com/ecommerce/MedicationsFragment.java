package msdemo.ayhan.com.ecommerce;

import android.os.Bundle;
import android.support.design.widget.Snackbar;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.GridView;
import android.widget.ListView;
import android.widget.Toast;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import java.lang.reflect.Array;
import java.util.ArrayList;


public class MedicationsFragment extends Fragment {

    ArrayList<MedicationModel> medications = new ArrayList<>();
    ListView medications_listview;
    MedicationsAdapter medications_adapter;
    View mView;
    View mMainView;
    public MedicationsFragment() {
        // Required empty public constructor
    }

    public static MedicationsFragment newInstance() {
        MedicationsFragment fragment = new MedicationsFragment();
        Bundle args = new Bundle();

        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (getArguments() != null) {

        }

    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        mView = inflater.inflate(R.layout.fragment_medications, container, false);
        mMainView = getActivity().findViewById(android.R.id.content);
        GetMedications();
        return mView;
    }
    private void GetMedications() {

        try {
            String [] params = {"medication/get-all-medications/", "GET", ""};


            new RestClientTask() {
                protected void onPostExecute(String result) {
                    try {
                        JsonObject response_json = new JsonParser().parse(result).getAsJsonObject();
                        String result_string = response_json.get("Result").toString().replaceAll("\"", "");
                        if (result_string.equals("Success")) {
                            String data_string = response_json.get("Data").toString();
                            JsonObject data_json = new JsonParser().parse(data_string).getAsJsonObject();
                            String status_string = data_json.get("result").toString();
                            JsonObject status_json = new JsonParser().parse(status_string).getAsJsonObject();
                            String register_status = status_json.get("Status").toString().replaceAll("\"", "");
                            if (register_status.equals("Success")) {
                                //String medications_string = status_json.get("Medications").toString().replaceAll("\"", "");
                                JsonArray medications_json = status_json.get("Medications").getAsJsonArray();
                                for (int i = 0; i < medications_json.size(); ++i) {
                                    JsonArray next_medication = medications_json.get(i).getAsJsonArray();
                                    Integer medication_id = next_medication.get(0).getAsInt();
                                    String medication_code = next_medication.get(1).toString().replaceAll("\"", "");;
                                    String medication_name = next_medication.get(2).toString().replaceAll("\"", "");;
                                    String medication_description = next_medication.get(3).toString().replaceAll("\"", "");;
                                    String medication_supplier = next_medication.get(4).toString().replaceAll("\"", "");;
                                    String medication_category_code = next_medication.get(5).toString().replaceAll("\"", "");;
                                    Float medication_price = next_medication.get(6).getAsFloat();
                                    Integer medication_stock = next_medication.get(7).getAsInt();
                                    String medication_category_name = next_medication.get(8).toString().replaceAll("\"", "");;
                                    medication.add(new MedicationModel(
                                            medication_id,
                                            medication_code,
                                            medication_name,
                                            medication_description,
                                            medication_supplier,
                                            medication_category_code,
                                            medication_price,
                                            medication_stock,
                                            medication_category_name));


                                }

                                medications_adapter = new MedicationsAdapter(medications, getActivity(), getView());
                                medications_listview = mView.findViewById(R.id.listview_medications);
                                medications_listview.setAdapter(medications_adapter);
                            }
                            else {

                            }
                            Snackbar.make(mMainView, "GetMedications: " + register_status, Snackbar.LENGTH_LONG)
                                    .setAction("No action", null).show();

                        }
                        else {
                            Snackbar.make(mMainView, "GetMedications Fail " + result, Snackbar.LENGTH_LONG)
                                    .setAction("No action", null).show();
                        }
                    }
                    catch (Exception ex) {

                    }


                }
            }.execute(params);
        }
        catch (Exception ex) {

        }
    }


    @Override
    public void onDetach() {
        super.onDetach();
    }


}
