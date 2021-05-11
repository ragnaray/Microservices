package msdemo.ayhan.com.ecommerce;

public class MedicationModel {
    int ID;
    String Code;
    String Name;
    String Description;
    String Supplier;
    String CategoryId;
    Float Price;
    int Stock;
    String CategoryName;

    public MedicationModel(int ID, String Code, String Name, String Description, String Supplier, String CategoryId, Float Price, int Stock, String CategoryName) {
        this.ID = ID;
        this.Code = Code;
        this.Name = Name;
        this.Description = Description;
        this.Supplier = Supplier;
        this.CategoryId = CategoryId;
        this.Price = Price;
        this.Stock = Stock;
        this.CategoryName = CategoryName;
    }

    public String getName() {
        return Name;
    }
    public String getCode() {
        return Code;
    }
    public Float getPrice() {
        return Price;
    }
    public int getID() {
        return ID;
    }
}
