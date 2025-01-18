price_a = float(input("Enter a price:"))
price_b = float(input("Enter another price:"))                      #inputing data


if price_a > price_b:                                               #By comparing the prices, for 3 situations: a>b , a<b , a==b,
    print("The first price is larger than the second one.")         #the code can give out the respective results.
elif price_a < price_b:
    print("The first price is smaller than the second one.")
elif price_a == price_b:
    print("The price are the same.")