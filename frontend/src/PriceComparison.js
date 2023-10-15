import React, { useState, useEffect } from "react";
import { Grid } from "@mui/material";
import StoreCard from "./StoreCard";
import axios from "axios";

const backendUrl = process.env.REACT_APP_BACKEND_URL;

const transformData = (backendData) => {
  const storeMap = {};

  Object.values(backendData)
    .flat()
    .forEach((entry) => {
      const storeName = entry.store.name;
      const productName = entry.product.name;
      const price = entry.price;

      if (!storeMap[storeName]) {
        storeMap[storeName] = {
          storeName,
          totalPrice: 0,
          items: [],
        };
      }

      storeMap[storeName].totalPrice += price;
      storeMap[storeName].items.push({ name: productName, price });
    });

  return Object.values(storeMap).sort((a, b) => a.totalPrice - b.totalPrice); // sort by total price
};

const PriceComparison = ({ items, zip_code, totalItems, loading}) => {
  const [storeData, setStoreData] = useState([]);

  useEffect(() => {
    const fetchPrices = async () => {
      try {
        const response = await axios.get(`${backendUrl}/prices`,{
          params: {
            item_names: items.map((item) => item.name).join(",") ,
            zip_code: zip_code
          }
        });
        const backendData = response.data;
        console.log("Received data from API:", backendData);
        const transformedData = transformData(backendData);
        console.log("Transformed Data:", transformedData);

        const data = response.data;

        // Transform the data into the desired structure
        let aggregatedData = {};

        for (let item in data) {
          for (let store in data[item]) {
            if (!aggregatedData[store]) {
              aggregatedData[store] = 0;
            }
            // Assume that we are taking the first price in the store's list for each item for simplicity
            aggregatedData[store] += Object.values(data[item][store])[0];
          }
        }

        setStoreData(transformedData);
      } catch (error) {
        console.error("Error fetching prices:", error);
      }
    };

    fetchPrices();
  }, [items, zip_code]);

  return (
    <Grid container direction="column" alignItems="center" spacing={3}>
      {storeData.map((data, index) => (
        <Grid item key={data.storeName} xs={12}>
          <StoreCard
            storeName={data.storeName}
            items={data.items}
            totalPrice={data.totalPrice}
            isCheapest={index === 0}
            totalItems={totalItems}
            loading={loading}
          />
        </Grid>
      ))}
    </Grid>
  );
};

export default PriceComparison;
