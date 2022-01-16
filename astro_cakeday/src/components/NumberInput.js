import React from "react";

const NumberInput = ({value, changeHandler}) => {
  return (
    <div>
      <input
        type="number"
        value={value}
        onChange={changeHandler}
      />
      <p></p>
    </div>
  );
};

export default NumberInput;
