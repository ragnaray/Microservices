package msdemo.ayhan.com.ecommerce;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.design.widget.Snackbar;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import org.json.JSONObject;


public class RegisterFragment extends Fragment {
    Button btn_register;
    EditText txt_username;
    EditText txt_fullname;
    EditText txt_password;
    EditText txt_email;
    View mView;
    View mMainView;

    public RegisterFragment() {
        // Required empty public constructor
    }

    public static RegisterFragment newInstance() {
        RegisterFragment fragment = new RegisterFragment();
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
        mView = inflater.inflate(R.layout.fragment_register, container, false);
        mMainView = getActivity().findViewById(android.R.id.content);

        txt_username = mView.findViewById(R.id.txt_user_name);
        txt_password = mView.findViewById(R.id.txt_password);
        txt_fullname = mView.findViewById(R.id.txt_full_name);
        txt_email = mView.findViewById(R.id.txt_email);
        btn_register = mView.findViewById(R.id.btn_register);

        btn_register.setOnClickListener((View v) -> {
            OnRegisterClick(v);
        });


        return mView;
    }
    private void OnRegisterClick(View view) {
        String user_name = txt_username.getText().toString();
        String password = txt_password.getText().toString();
        String full_name = txt_fullname.getText().toString();
        String email = txt_email.getText().toString();

        try {
             /*String jsonString = new JSONObject()
                    .put("UserName", user_name)
                    .put("Password", password).toString();*/
            JsonObject post_json = new JsonObject();
            post_json.addProperty("UserName", user_name);
            post_json.addProperty("Password", password);
            post_json.addProperty("FullName", full_name);
            post_json.addProperty("Email", email);
            post_json.addProperty("Credit", 100);

            String [] params = {"customer/add-user/", "POST", post_json.toString()};


            new RestClientTask() {
                protected void onPostExecute(String result) {

                    JsonObject response_json = new JsonParser().parse(result).getAsJsonObject();
                    String result_string = response_json.get("Result").toString().replaceAll("\"", "");
                    if (result_string.equals("Success")) {
                        String data_string = response_json.get("Data").toString();
                        JsonObject data_json = new JsonParser().parse(data_string).getAsJsonObject();
                        String status_string = data_json.get("result").toString();
                        JsonObject status_json = new JsonParser().parse(status_string).getAsJsonObject();
                        String register_status = status_json.get("Status").toString().replaceAll("\"", "");
                        if (register_status.equals("Success")) {
                            //Not doing anything special
                        }
                        else {

                        }
                        Snackbar.make(mView, "Register: " + register_status, Snackbar.LENGTH_LONG)
                                .setAction("No action", null).show();

                    }
                    else {
                        Snackbar.make(mView, "Register Fail " + result, Snackbar.LENGTH_LONG)
                                .setAction("No action", null).show();
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
