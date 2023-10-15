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
import Snackbar from "@mui/material/Snackbar";
import ItemInput from "./ItemInput";
import PriceComparison from "./PriceComparison";
import axios from "axios";
const backendUrl = process.env.REACT_APP_BACKEND_URL;

const App = () => {
  const [loading, setLoading] = useState("idle");
  const [fetchPromises, setFetchPromises] = useState([]);
  const [items, setItems] = useState([]);
  const [currentItem, setCurrentItem] = useState("");
  const [showComparison, setShowComparison] = useState(false);
  const [currentZip, setCurrentZip] = useState("");
  const [notification, setNotification] = useState({
    open: false,
    message: "",
  });

  const displayNotification = (message) => {
    setNotification({ open: true, message });
  };

  const closeNotification = () => {
    setNotification({ open: false, message: "" });
  };

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

      const fetchPrice = axios.post("/prices", {
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
          .then((response) => {
            return {
              itemName: currentItem,
              price: response.data.price,
            };
          })
          .catch((error) => {
            if (error.response && error.response.status === 404) {
              // Remove the item from the list
              setItems((prevItems) =>
                prevItems.filter((item) => item.name !== currentItem)
              );

              // Display the notification
              displayNotification(
                `Item "${currentItem}" couldn't be found nearby. Try entering a similar word or specific brand.`
              );
            }
          })
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
        if (result.status === "fulfilled" && result.value) {
            const index = updatedItems.findIndex(
                (item) => item.name === result.value.itemName
            );
            if (index !== -1) {
                updatedItems[index] = {
                    ...updatedItems[index],
                    price: result.value.price,
                };
            }
        } else if (result.status === "rejected") {
            const index = updatedItems.findIndex(
                (item) => item.name === result.reason.itemName
            );
            if (index !== -1) {
                const itemName = updatedItems[index].name;
                updatedItems.splice(index, 1); // Remove the item from the list

                // Display the notification
                displayNotification(
                    `Item "${itemName}" couldn't be found nearby. Try entering a similar word or specific brand.`
                );
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
      <>
        <Snackbar
          anchorOrigin={{ vertical: "top", horizontal: "center" }}
          open={notification.open}
          onClose={closeNotification}
          message={notification.message}
          autoHideDuration={6000}
        />
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
                showComparison={showComparison}
              />

              <Button
                variant="contained"
                color="primary"
                onClick={handleAddToList}
                style={{ marginTop: "0.5rem" }}
              >
              {loading === "button" ? (
                <span
                  style={{
                    display: "inline-block",
                    width: "24px",
                    height: "24px",
                  }}
                >
                  <CircularProgress size={24} color="inherit" />
                </span>
              ) : (
                "Add Item"
              )}
            </Button>
            {!showComparison && (
              <Button
                variant="contained"
                onClick={handleCheckPricesDebounced}
                disabled={items.length === 0}
                style={{ marginTop: "0.5rem" }}
              >
                Check Prices
            </Button>
            )}
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
          {showComparison && (
            <PriceComparison items={items} zip_code={currentZip} totalItems={items.length} loading={loading}/>
          )}
        </Container>
      </>
    </>
  );
};

export default App;
