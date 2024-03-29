package msdemo.rxmed.com.ecommerce;

public class OrderModel {
    int Id;
    String Code;
    String UserId;
    String MedicationId;
    String MedicationName;
    Float Price;
    int OrderStatus;
    int StockStatus;
    int CreditStatus;
    int Stock;
    String OrderTime;
    Float Credit;
    //{"GUID":"7a837981-4a1b-4a21-b226-8e2947d08e60","USERID":"jon","MEDICATION":"fcc6fe7b-1784-4f47-8efa-137b19a876ed",
    // "MEDICATIONNAME":"Hot Laptop","PRICE":19.0,"ORDERSTATUS":1,"STOCKSTATUS":3,"CREDITSTATUS":2,"TIME":"2018-24-12 01:36:53","CREDIT":5.0,"STOCK":43}
    public OrderModel(String Code, String UserId, String MedicationId, String MedicationName, Float Price,
                      int OrderStatus, int StockStatus, int CreditStatus, String OrderTime, int Stock, Float Credit) {
       this.Code = Code;
       this.UserId = UserId;
       this.MedicationId = MedicationId;
       this.MedicationName = MedicationName;
       this.Price = Price;
       this.OrderStatus = OrderStatus;
       this.StockStatus = StockStatus;
       this.CreditStatus = CreditStatus;
       this.OrderTime = OrderTime;
       this.Stock = Stock;
       this.Credit = Credit;
    }

    public int getId() {return Id;}
    public String getCode() {
        return Code;
    }
    public String getMedicationId() { return MedicationId; }
    public String getMedicationName() { return MedicationName; }
    public Float getPrice() {
        return Price;
    }
    public int getOrderStatus() {
        return OrderStatus;
    }
    public int getStockStatus() {
        return StockStatus;
    }
    public int getCreditStatus() {
        return CreditStatus;
    }
    public Float getCredit() {return Credit;}
    public int getStock() {
        return Stock;
    }
    public String getOrderTime() { return OrderTime; }
}
