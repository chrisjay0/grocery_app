import React, { useState, useEffect, useRef } from "react";
import {
  Container,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Typography,
  CircularProgress,
  Button,
  Box,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import ItemInput from "./ItemInput";
import PriceComparison from "./PriceComparison";
import axios from "axios";

const App = () => {
  const [loading, setLoading] = useState("idle");
  const [fetchPromises, setFetchPromises] = useState([]);
  const [items, setItems] = useState([]);
  const [currentItem, setCurrentItem] = useState("");
  const [showComparison, setShowComparison] = useState(false);
  const [currentZip, setCurrentZip] = useState("");

  const shouldStopLoading = useRef(false);
  useEffect(() => {
    if (fetchPromises.length === 0 && loading !== "idle") {
      setLoading("idle");
    }
  }, [fetchPromises, loading]);

  const handleAddToList = () => {
    if (currentItem.trim()) {
      setItems((prevItems) => [
        ...prevItems,
        { name: currentItem, price: null },
      ]);
      setCurrentItem("");

      const fetchPrice = axios.post("http://127.0.0.1:5000/prices", {
        item_name: currentItem,
        zip_code: currentZip,
      });

      if (showComparison) {
        setLoading("button");
        shouldStopLoading.current = true;
      }

      setFetchPromises((prevPromise) => [
        ...prevPromise,
        fetchPrice
          .then((response) => ({
            itemName: currentItem,
            price: response.data.price,
          }))
          .finally(() => {
            if (shouldStopLoading.current) {
              setLoading("idle");
              shouldStopLoading.current = false;
            }
          }),
      ]);
    }
  };



  const handleRemoveItem = (indexToRemove) => {
    setItems((prevItems) => {
      const updatedItems = prevItems.filter(
        (_, index) => index !== indexToRemove
      );
      if (updatedItems.length === 0) {
        setShowComparison(false);
      }
      return updatedItems;
    });
  };

  const handleCheckPrices = async () => {
    setLoading("general");
    let results = [];

    try {
      results = await Promise.allSettled(fetchPromises);
    } catch (error) {
      alert("An unexpected error occurred. Please try again.");
    } finally {
      setFetchPromises([]); // Clear promises once they've been awaited
    }

    // Create a copy of the current items
    const updatedItems = [...items];

    results.forEach((result) => {
      if (result.status === "fulfilled") {
        const index = updatedItems.findIndex(
          (item) => item.name === result.value.itemName
        );
        if (index !== -1) {
          updatedItems[index] = {
            ...updatedItems[index],
            price: result.value.price,
          };
        }
      }
    });

    // Update the items state with the new array
    setItems(updatedItems);

    // Now check the updatedItems array directly
    if (updatedItems.some((item) => item.price === null)) {
      alert("Some prices could not be fetched. Please try again.");
    } else {
      setShowComparison(true);
    }

    setLoading("idle");
  };

  const debounce = (func, delay) => {
    let debounceTimer;
    return function (...args) {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => func.apply(this, args), delay);
    };
  };

  const handleCheckPricesDebounced = debounce(handleCheckPrices, 500);

  return (
    <>
      {loading === "general" && (
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            height: "100vh",
            width: "100vw",
            position: "fixed",
            top: 0,
            left: 0,
            zIndex: 1000,
            backgroundColor: "rgba(255, 255, 255, 0.7)",
          }}
        >
          <CircularProgress />
        </div>
      )}

      <Container
        maxWidth="lg"
        style={{
          display: "flex",
          justifyContent: showComparison ? "flex-start" : "center",
          alignItems: "flex-start",
          paddingTop: "10vh",
        }}
      >
        <div
          style={{
            marginLeft: showComparison ? "10rem" : "0rem",
            marginRight: showComparison ? "-10rem" : "0rem",
          }}
        >
          <Typography
            variant="h4"
            component="h1"
            align={showComparison ? "center" : "center"}
            gutterBottom
          >
            Grocery Price Comparator
          </Typography>
          <Box
            display="flex"
            flexDirection="column"
            alignItems={showComparison ? "" : "center"}
          >
            <ItemInput
              currentItem={currentItem}
              onItemChange={setCurrentItem}
              onAddItem={handleAddToList}
              currentZip={currentZip}
              onZipChange={setCurrentZip}
            />

            <Button
              variant="contained"
              color="primary"
              onClick={handleAddToList}
              style={{ marginTop: "0.5rem" }}
            >
              Add to List
            </Button>

            <Button
              variant="contained"
              onClick={handleCheckPricesDebounced}
              disabled={items.length === 0}
              style={{ marginTop: "0.5rem" }}
              startIcon={
                loading === "button" ? <CircularProgress size={24} /> : null
              }
            >
              {loading === "button" ? "" : "Check Prices"}
            </Button>
          </Box>
          <List style={{ marginTop: "1rem" }}>
            {items.map((item, index) => (
              <ListItem key={index}>
                <ListItemText primary={item.name} />
                <ListItemSecondaryAction>
                  <IconButton
                    edge="end"
                    aria-label="delete"
                    onClick={() => handleRemoveItem(index)}
                  >
                    <CloseIcon />
                  </IconButton>
                </ListItemSecondaryAction>
              </ListItem>
            ))}
          </List>
        </div>
        {showComparison && <PriceComparison items={items} />}
      </Container>
    </>
  );
};

export default App;
