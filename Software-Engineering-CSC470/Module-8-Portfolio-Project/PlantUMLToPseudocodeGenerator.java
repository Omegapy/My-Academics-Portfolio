/*
        Program Name: PlantUML Class Diagram To Pseudocode Generator Version-5
        Author: Alexander (Alex) Ricciardi
        Date: 01/23/2025

        Program Description:
        A small Java program that translates PlantUML class diagrams to pseudocode by parsing the PlantUML code 
        using Regex and Java methods. The program also generates comments based on CRUD operations.
    
        
*/

/*-------------------
 |     Packages     |
 -------------------*/
package plantUMLClassDiagramToPseudocode;


/*---------------------------
|    Imported modules      |
---------------------------*/
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


/**
 * Takes a PlantUML class diagram code as inputs and outputs a pseudocode of it.
 * It extracts class elements such as definitions, attributes, methods, and inheritance relationships.
 * 
 * @author Alexander Ricciardi
 * @version 5.0
 * @date 01/23/2025
 */
public class PlantUMLToPseudocodeGenerator {

	// -------------------------------------------------------------------------------------------------
    /*----------------------
     |    Helper classes   |
     ----------------------*/
	
	/**
     * The UMLClass helper class encapsulates data from each UML class parsed from the PlantUML code input.
     * It stores the class name, its stereotypes (entity, control, or table), its attributes,
     * its methods, and the name of its parent class (if any).
     */
    static class UMLClass {
        String name;
        String stereotype; // entity, control, table, etc.
        List<String> attributes = new ArrayList<>();
        List<String> methods = new ArrayList<>();
        String parent = null; // for inheritance (if any)

        UMLClass(String name, String stereotype) {
            this.name = name;
            // stereotype to lowercase if present.
            this.stereotype = (stereotype != null) ? stereotype.toLowerCase() : "";
        }
    }
    
    // -------------------------------------------------------------------------------------------------
    /*----------------
     |    Methods   |
     ----------------*/
    
    /**
     * Generates the pseudocode based on method signatures (e.g. "createTruck(truckId: Integer, truckDtls): Void"),
     * returns a list of pseudocode lines representing methods including comments bases on CRUD operations.
     */
    private static List<String> generateMethodPseudocode(String rawMethod, String className) {
    	
    	//------- Parameter and Return Type Extraction -------
    	// This section extracts the return type from the method signature and separates it from the parameters.
        List<String> lines = new ArrayList<>();
        String methodSignature = rawMethod.trim();
        String returnType = "";
        // Split the signature on the last colon (:) to separate the return type if it exists.
        int colonIndex = methodSignature.lastIndexOf(":");
        if (colonIndex != -1) {
            returnType = methodSignature.substring(colonIndex + 1).trim();
            methodSignature = methodSignature.substring(0, colonIndex).trim();
        }
        
        //------- Parameter Reordering -------
    	// Reorders each parameter from "name: Type" to "Type name" to match pseudocode conventions.
        int openParenIndex = methodSignature.indexOf("(");
        int closeParenIndex = methodSignature.lastIndexOf(")");
        String processedMethodSignature = methodSignature;
        if (openParenIndex != -1 && closeParenIndex != -1 && closeParenIndex > openParenIndex) {
            String methodNamePart = methodSignature.substring(0, openParenIndex).trim();
            String params = methodSignature.substring(openParenIndex + 1, closeParenIndex).trim();
            if (!params.isEmpty()) {
                // Use a method to split parameters without splitting inside array brackets.
                List<String> paramList = splitParameters(params);
                List<String> newParams = new ArrayList<>();
                for (String param : paramList) {
                    param = param.trim();
                    if (param.contains(":")) {
                        // Reorder parameter from "name: Type" to "Type name"
                        String[] parts = param.split(":");
                        if (parts.length == 2) {
                            String paramName = parts[0].trim();
                            String paramType = parts[1].trim();
                            newParams.add(paramType + " " + paramName);
                        } else {
                            newParams.add(param);
                        }
                    } else {
                        newParams.add(param);
                    }
                }
                String processedParams = String.join(", ", newParams);
                processedMethodSignature = methodNamePart + "(" + processedParams + ")";
            }
        }
        
        //------- Header construction -------
    	// This section constructs the method header line using the reordered parameters and adds the return type.
        String headerLine = "    public " + processedMethodSignature;
        if (!returnType.equalsIgnoreCase("Void") && !returnType.isEmpty()) {
            headerLine += " -> " + returnType;
        }
        headerLine += ":";
        lines.add(headerLine);
        
        //------- Comment generation -------
    	// Generates a comment based on the method name to indicate its functionality base on CRUD operations.
        String comment = "        // ... ";
        // We extract the method name for analysis (before the '(').
        int parenIndex = processedMethodSignature.indexOf("(");
        String methodName = (parenIndex != -1) ? processedMethodSignature.substring(0, parenIndex).trim() : processedMethodSignature;
        if (methodName.startsWith("create")) {
            if (className.endsWith("_table")) {
                String entityName = className.substring(0, className.indexOf("_table")).toLowerCase();
                comment += "Insert " + entityName + " record into the database";
            } else {
                comment += "Creation logic here";
            }
        } else if (methodName.startsWith("read")) {
            if (className.endsWith("_table")) {
                String entityName = className.substring(0, className.indexOf("_table")).toLowerCase();
                comment += "Retrieve " + entityName + " record from the database";
            } else {
                comment += "Retrieval logic here";
            }
        } else if (methodName.startsWith("update")) {
            if (className.endsWith("_table")) {
                String entityName = className.substring(0, className.indexOf("_table")).toLowerCase();
                comment += "Update " + entityName + " record in the database";
            } else {
                comment += "Update logic here";
            }
        } else if (methodName.startsWith("delete")) {
            if (className.endsWith("_table")) {
                String entityName = className.substring(0, className.indexOf("_table")).toLowerCase();
                comment += "Delete " + entityName + " record from the database";
            } else {
                comment += "Deletion logic here";
            }
        } else if (methodName.startsWith("drive")) {
            comment += "Logic to simulate driving";
        } else {
            comment += "Method logic here";
        }
        lines.add(comment);
        
        //------- Return statement ------- 
    	// Builds the return statement line based on the method's return type.
        String returnLine = "        return ";
        if (returnType.equalsIgnoreCase("Void") || returnType.isEmpty()) {
            returnLine += "void";
        } else {
            returnLine += returnType;
        }
        lines.add(returnLine);
        
        return lines;
    } 
    
    // -------------------------------------------------------------------------------------------------
    
    /**
     * Splits the parameter string into individual parameters while keeping commas inside square brackets intact.
     * (e.g. Array[Integer, Interger])
     *
     * @param params The parameter list as a string.
     * @return A list of parameter strings.
     */
    private static List<String> splitParameters(String params) {
        List<String> result = new ArrayList<>();
        StringBuilder current = new StringBuilder();
        int bracketLevel = 0;
        for (int i = 0; i < params.length(); i++) {
            char c = params.charAt(i);
            if (c == '[') {
                bracketLevel++;
            } else if (c == ']') {
                if (bracketLevel > 0) {
                    bracketLevel--;
                }
            } else if (c == ',' && bracketLevel == 0) {
                result.add(current.toString());
                current.setLength(0);
                continue;
            }
            current.append(c);
        }
        if (current.length() > 0) {
            result.add(current.toString());
        }
        return result;
    }
    
    // ---------------------------------------------------------------------------------------------------------
    /*--------------------
    |    Main Method    |
    --------------------*/
    
    /**
     *  Main method: Parses the PlantUML diagram and outputs the pseudocode.
     */
    public static void main(String[] args) {
        // Text block of the The PlantUML code 
        String plantUML = """
            @startuml
			'
			' Entity Classes
			'
			class "Driver" <<entity>> {
			  -driverId: Integer
			  -lastName: String
			  -cars: List<Car>
			}
			
			class "Vehicle" <<entity>> {
			  -vehicleId: Integer
			  -vinNum: String
			  -driverIds: List<Integer>
			  +drive()
			}
			
			class "Truck" <<entity>> {
			  -truckId: Integer
			  -truckType: String
			}
			
			class "Car" <<entity>> {
			  -carId: Integer
			  -carType: String
			}
			
			'
			' Control Class
			'
			class "DriverCarManager" <<control>> {
			+createDriver(driverId: Integer, driverDtls): Void
			+readDriver(driverId: Integer): driverDtls
			+updateDriver(driverId: Integer, driverDtls): Void
			+deleteDriver(driverId: Integer): Void
			
			+createVehicle(vehiculeId: Integer, vehicleDtls): Void
			+readVehicle(vehicleId: Integer): vehicleDtls
			+updateVehicle(carId: Integer): Void
			+deleteVehicle(carId: Integer): Void
			
			+createCar(carId: Integer, carDtls): Void
			+readCar(carId: Integer): carDtls
			+updateCar(carId: Integer, carDtls): Void
			+deleteCar(carId: Integer): Void
			
			+createTruck(truckId: Integer, truckDtls): Void
			+readTruck(truckId: Integer): truckDtls
			+updateTruck(truckId: Integer, truckDtls): Void
			+deleteTruck(truckId: Integer): Void
			
			+createDriverVehicle(driverVehicleId: Array[Integer, Integer], driverVehicleDtls): Void
			+readDriverVehicle(driverVehicleId: Integer): driverVehicleDtls
			+updateDriverVehicle(driverVehicleId: Integer, driverVehicleDtls): Void
			+deleteDriverVehicle(driverVehicleId: Integer): Void
			}
			
			'
			' Table Classes
			'
			class "Driver_table" <<table>> {
			  -driverId: Integer
			  -driverName: String
			
			  +createDriver(driverId: Integer, driverDtls): Void
			  +readDriver(driverId: Integer): driverDtls
			  +updateDriver(driverId: Integer, driverDtls): Void
			  +deleteDriver(driverId: Integer): Void
			}
			
			class "Vehicle_table" <<table>> {
			  -vehicleId: Integer
			  -vinNum: String
			
			  +createVehicle(vehicleId: Integer, vehicleDtls): Void
			  +readVehicle(vehicleId: Integer): vehicleDtls
			  +updateVehicle(carId: Integer): Void
			  +deleteVehicle(carId: Integer): Void
			}
			
			class "Driver_Vehicle_table" <<table>> {
			  -driverVehicleId: [Integer, Integer]
			  -driverId: Integer
			  -vehicleId: Integer
			
			  +createDriverVehicle(driverVehicleId: Array[Integer, Integer], driverVehicleDtls): Void
			  +readDriverVehicle(driverVehicleId: Integer): driverVehicleDtls
			  +updateDriverVehicle(driverVehicleId: Integer, driverVehicleDtls): Void
			  +deleteDriverVehicle(driverVehicleId: Integer): Void
			}
			
			class "Truck_table" <<table>> {
			  -truckId: Integer
			  -truckType: String
			
			  +createTruck(truckId: Integer, truckDtls): Void
			  +readTruck(truckId: Integer): truckDtls
			  +updateTruck(truckId: Integer, truckDtls): Void
			  +deleteTruck(truckId: Integer): Void
			}
			
			class "Car_table" <<table>> {
			  -carId: Integer
			  -carType: String
			
			  +createCar(carId: Integer, carDtls): Void
			  +readCar(carId: Integer): carDtls
			  +updateCar(carId: Integer, carDtls): Void
			  +deleteCar(carId: Integer): Void
			}
			
			'
			' Relationships
			'
			' Inheritance (Vehicle is a superclass of Truck and Car)
			Vehicle <|-- Truck
			Vehicle <|-- Car
			
			' Driver can drive many Vehicles (1..N)
			Driver "1" --> "1..N" Vehicle : drives
			
			' Driver and Vehicle both use the DriverCarManager
			Driver "1..N" --> "1" DriverCarManager : uses
			Vehicle "1..N" --> "1" DriverCarManager : uses
			
			' DriverCarManager uses the database tables
			DriverCarManager --> Driver_table : uses
			DriverCarManager --> Vehicle_table : uses
			DriverCarManager --> Car_table : uses
			DriverCarManager --> Truck_table : uses
			DriverCarManager --> Driver_Vehicle_table : uses
			
			' Driver_Vehicle_table use the Driver_table and Vehicle_table
			Driver_Vehicle_table --> Driver_table : uses
			Driver_Vehicle_table --> Vehicle_table : uses
			
			' Car_table and Truck_table use the Vehicle_table
			Car_table -->  Vehicle_table : uses
			Truck_table -->  Vehicle_table : uses
			
			@enduml
            """;

        // A list to hold all parsed classes.
        List<UMLClass> classes = new ArrayList<>();
        // A list to hold relationship lines (we will later process inheritance).
        List<String> relationshipLines = new ArrayList<>();

        //------- Regex patterns for class parsing -------
    	// Regex patterns are used to define class definitions and class members.
        Pattern classPattern = Pattern.compile("^class\\s+\"([^\"]+)\"(?:\\s+<<([^>]+)>>)?\\s*\\{?");
        Pattern memberPattern = Pattern.compile("^([+-])(.*)");

        Scanner scanner = new Scanner(plantUML);
        boolean insideClass = false;
        UMLClass currentClass = null;
        
        //------- Parse PlantUML input to extract class definitions ------- 
    	// This loop goes through each line of the PlantUML input and extracts class information.
        while (scanner.hasNextLine()) {
            String line = scanner.nextLine().trim();
            // Skip empty lines or lines that are comments or control directives.
            if (line.isEmpty() || line.startsWith("'") ||
                line.startsWith("@startuml") || line.startsWith("@enduml")) {
                continue;
            }
            // Check for a class definition.
            Matcher classMatcher = classPattern.matcher(line);
            if (classMatcher.find()) {
                String className = classMatcher.group(1);
                String stereotype = classMatcher.group(2);
                currentClass = new UMLClass(className, stereotype);
                insideClass = true;
                continue;
            }
            if (insideClass) {
                // End of class block.
                if (line.equals("}")) {
                    classes.add(currentClass);
                    insideClass = false;
                    currentClass = null;
                    continue;
                }
                // Process members (attributes or methods).
                Matcher memberMatcher = memberPattern.matcher(line);
                if (memberMatcher.find()) {
                    String content = memberMatcher.group(2).trim();
                    if (content.contains("(") && content.contains(")")) {
                        currentClass.methods.add(content);
                    } else {
                        currentClass.attributes.add(content);
                    }
                }
                continue;
            }
            // Outside class blocks, capture relationship lines.
            if (line.contains("<|--") || line.contains("-->")) {
                relationshipLines.add(line);
            }
        }
        scanner.close();

        //------- Maps Class Inheritance -------
    	// Creates a map of class names to UMLClass objects.
        Map<String, UMLClass> classMap = new HashMap<>();
        for (UMLClass cls : classes) {
            classMap.put(cls.name, cls);
        }
        // Using Regex to process inheritance relationships to update child classes.
        Pattern inheritancePattern = Pattern.compile("^(\\S+)\\s*<\\|--\\s*(\\S+)");
        for (String rel : relationshipLines) {
            Matcher inhMatcher = inheritancePattern.matcher(rel);
            if (inhMatcher.find()) {
                String parentName = inhMatcher.group(1);
                String childName = inhMatcher.group(2);
                if (classMap.containsKey(childName)) {
                    classMap.get(childName).parent = parentName;
                }
            }
        }
        
        //------- Output pseudocode for each parsed Class -------
    	// Prints the header and pseudocode for each class.
        // Print the system header.
        System.out.println("/*");
        System.out.println("      Vehicle Database Management System Class Pseudocode Version-5");
        System.out.println("      Alexander Ricciardi");
        System.out.println("      January 23, 2025");
        System.out.println("*/");

        // Print each class in its own section.
        for (UMLClass cls : classes) {
            System.out.println("/------------------------------------------------------------------------------");
            System.out.println("// " + cls.name + " Class");
            System.out.println("/------------------------------------------------------------------------------");
            // Print class signature with inheritance if applicable.
            if (cls.parent != null) {
                System.out.println("class " + cls.name + " extends " + cls.parent + ":");
            } else {
                System.out.println("class " + cls.name + ":");
            }
            // Print attributes with data type first, variable name second.
            for (String attr : cls.attributes) {
                // Assume the attribute is in the form "variableName: DataType"
                String[] parts = attr.split(":");
                if (parts.length == 2) {
                    String varName = parts[0].trim();
                    String dataType = parts[1].trim();
                    System.out.println("    private " + dataType + " " + varName);
                } else {
                    System.out.println("    private " + attr);
                }
            }
            // Add a blank line if there are both attributes and methods.
            if (!cls.attributes.isEmpty() && !cls.methods.isEmpty()) {
                System.out.println();
            }
            // Print methods using formatting helper.
            for (String method : cls.methods) {
                List<String> methodLines = generateMethodPseudocode(method, cls.name);
                for (String lineOut : methodLines) {
                    System.out.println(lineOut);
                }
                System.out.println(); // Blank line after each method.
            }
            System.out.println(); // Blank line after each class.
        }
    }
    
}
