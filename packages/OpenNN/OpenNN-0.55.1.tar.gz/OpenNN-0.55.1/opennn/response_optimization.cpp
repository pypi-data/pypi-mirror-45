/****************************************************************************************************************/
/*                                                                                                              */
/*   OpenNN: Open Neural Networks Library                                                                       */
/*   www.opennn.net                                                                                             */
/*                                                                                                              */
/*   R E S P O N S E   O P T I M I Z A T I O N   C L A S S                                                      */
/*                                                                                                              */
/*   Artificial Intelligence Techniques SL                                                                      */
/*   artelnics@artelnics.com                                                                                    */
/*                                                                                                              */
/****************************************************************************************************************/

// OpenNN includes

#include "response_optimization.h"

namespace OpenNN
{

// DEFAULT CONSTRUCTOR

/// Default constructor. 
/// It creates a scaling layer object with no scaling neurons. 

ResponseOptimization::ResponseOptimization()
{   
}


ResponseOptimization::ResponseOptimization(NeuralNetwork* new_neural_network_pointer)
{
    neural_network_pointer = new_neural_network_pointer;

    const size_t inputs_number = neural_network_pointer->get_inputs_number();
    const size_t outputs_number = neural_network_pointer->get_outputs_number();

    inputs_conditions.set(inputs_number, Between);
    outputs_conditions.set(outputs_number, Minimum);

    inputs_minimums = neural_network_pointer->get_scaling_layer_pointer()->get_minimums();
    inputs_maximums = neural_network_pointer->get_scaling_layer_pointer()->get_maximums();

    outputs_minimums = neural_network_pointer->get_unscaling_layer_pointer()->get_minimums();
    outputs_maximums = neural_network_pointer->get_unscaling_layer_pointer()->get_maximums();
}


// DESTRUCTOR

/// Destructor.

ResponseOptimization::~ResponseOptimization()
{
}


void ResponseOptimization::set_input_condition(const string& name, const ResponseOptimization::Condition& condition, const Vector<double>& values)
{
    const size_t index = neural_network_pointer->get_inputs_pointer()->get_index(name);

    set_input_condition(index, condition, values);
}


void ResponseOptimization::set_output_condition(const string& name, const ResponseOptimization::Condition& condition, const Vector<double>& values)
{
    const size_t index = neural_network_pointer->get_outputs_pointer()->get_index(name);

    set_output_condition(index, condition, values);
}


void ResponseOptimization::set_input_condition(const size_t& index, const ResponseOptimization::Condition& condition, const Vector<double>& values)
{
    inputs_conditions[index] = condition;

    ostringstream buffer;

    switch(condition)
    {
        case Minimum:

            if(values.size() != 0)
            {
                buffer << "OpenNN Exception: ResponseOptimization class.\n"
                       << "void set_input_condition() method.\n"
                       << "For Minimum condition, size of values must be 0.\n";

                throw logic_error(buffer.str());
            }

        return;

        case Maximum:

            if(values.size() != 0)
            {
                buffer << "OpenNN Exception: ResponseOptimization class.\n"
                       << "void set_input_condition() method.\n"
                       << "For Maximum condition, size of values must be 0.\n";

                throw logic_error(buffer.str());
            }

        return;

        case EqualTo:

            if(values.size() != 1)
            {
                buffer << "OpenNN Exception: ResponseOptimization class.\n"
                       << "void set_input_condition() method.\n"
                       << "For LessEqualTo condition, size of values must be 1.\n";

                throw logic_error(buffer.str());
            }

            inputs_minimums[index] = values[0];
            inputs_maximums[index] = values[0];

        return;

        case LessEqualTo:

            if(values.size() != 1)
            {
                buffer << "OpenNN Exception: ResponseOptimization class.\n"
                       << "void set_input_condition() method.\n"
                       << "For LessEqualTo condition, size of values must be 1.\n";

                throw logic_error(buffer.str());
            }

            inputs_maximums[index] = values[0];

        return;

        case GreaterEqualTo:

            if(values.size() != 1)
            {
                buffer << "OpenNN Exception: ResponseOptimization class.\n"
                       << "void set_input_condition() method.\n"
                       << "For LessEqualTo condition, size of values must be 1.\n";

                throw logic_error(buffer.str());
            }

            inputs_minimums[index] = values[0];

        return;

        case Between:

            if(values.size() != 1)
            {
                buffer << "OpenNN Exception: ResponseOptimization class.\n"
                       << "void set_input_condition() method.\n"
                       << "For Between condition, size of values must be 2.\n";

                throw logic_error(buffer.str());
            }

            inputs_minimums[index] = values[0];
            inputs_maximums[index] = values[1];

        return;

        default:
        {
           buffer << "OpenNN Exception: ResponseOptimization class.\n"
                  << "void set_input_condition() method.\n"
                  << "Unknown condition.\n";

           throw logic_error(buffer.str());
        }
    }
}


void ResponseOptimization::set_output_condition(const size_t& index, const ResponseOptimization::Condition& condition, const Vector<double>& values)
{
    outputs_conditions[index] = condition;

    ostringstream buffer;

    switch(condition)
    {
        case Minimum:

            if(values.size() != 0)
            {
                buffer << "OpenNN Exception: ResponseOptimization class.\n"
                       << "void set_output_condition() method.\n"
                       << "For Minimum condition, size of values must be 0.\n";

                throw logic_error(buffer.str());
            }

        return;

        case Maximum:

            if(values.size() != 0)
            {
                buffer << "OpenNN Exception: ResponseOptimization class.\n"
                       << "void set_output_condition() method.\n"
                       << "For Maximum condition, size of values must be 0.\n";

                throw logic_error(buffer.str());
            }

        return;

        case EqualTo:

            if(values.size() != 1)
            {
                buffer << "OpenNN Exception: ResponseOptimization class.\n"
                       << "void set_output_condition() method.\n"
                       << "For LessEqualTo condition, size of values must be 1.\n";

                throw logic_error(buffer.str());
            }

            outputs_minimums[index] = values[0];
            outputs_maximums[index] = values[0];

        return;

        case LessEqualTo:

            if(values.size() != 1)
            {
                buffer << "OpenNN Exception: ResponseOptimization class.\n"
                       << "void set_output_condition() method.\n"
                       << "For LessEqualTo condition, size of values must be 1.\n";

                throw logic_error(buffer.str());
            }

            outputs_maximums[index] = values[0];

        return;

        case GreaterEqualTo:

            if(values.size() != 1)
            {
                buffer << "OpenNN Exception: ResponseOptimization class.\n"
                       << "void set_output_condition() method.\n"
                       << "For LessEqualTo condition, size of values must be 1.\n";

                throw logic_error(buffer.str());
            }

            outputs_minimums[index] = values[0];

        return;

        case Between:

            if(values.size() != 1)
            {
                buffer << "OpenNN Exception: ResponseOptimization class.\n"
                       << "void set_output_condition() method.\n"
                       << "For Between condition, size of values must be 2.\n";

                throw logic_error(buffer.str());
            }

            outputs_minimums[index] = values[0];
            outputs_maximums[index] = values[1];

        return;

        default:
        {
           buffer << "OpenNN Exception: ResponseOptimization class.\n"
                  << "void set_output_condition() method.\n"
                  << "Unknown condition.\n";

           throw logic_error(buffer.str());
        }
    }
}


Matrix<double> ResponseOptimization::calculate_inputs() const
{
    const size_t inputs_number = neural_network_pointer->get_inputs_number();

    Matrix<double> inputs(samples_number, inputs_number);

    for(size_t i = 0; i < samples_number; i++)
    {
        for(size_t j = 0; j < inputs_number; j++)
        {
            inputs(i,j) = calculate_random_uniform(inputs_minimums[j], inputs_maximums[j]);
        }
    }

    return inputs;
}


Matrix<double> ResponseOptimization::calculate_envelope() const
{
    const size_t inputs_number = neural_network_pointer->get_inputs_number();
    const size_t outputs_number = neural_network_pointer->get_outputs_number();

    const Matrix<double> inputs = calculate_inputs();

    const Matrix<double> outputs = neural_network_pointer->calculate_outputs(inputs);

    Matrix<double> envelope = inputs.assemble_columns(outputs);

    for(size_t i = 0; i < outputs_number; i++)
    {
        envelope = envelope.filter_column_minimum_maximum(inputs_number+i, outputs_minimums[i], outputs_maximums[i]);
    }

    return envelope;
}


ResponseOptimization::Results* ResponseOptimization::perform_optimization() const
{
    Results* results = new Results();

    const Matrix<double> envelope = calculate_envelope();

//    cout << envelope << endl;


    const size_t samples_number = envelope.get_rows_number();
    const size_t inputs_number = neural_network_pointer->get_inputs_number();
    const size_t outputs_number = neural_network_pointer->get_outputs_number();

    Vector<double> objective(samples_number, 0.0);

    for(size_t i = 0; i < samples_number; i++)
    {
        for(size_t j = 0; j < inputs_number; j++)
        {
            if(inputs_conditions[j] == Minimum)
            {
                objective[i] += envelope(i,j);
            }
            else if(inputs_conditions[j] == Maximum)
            {
                objective[i] += -envelope(i,j);
            }
        }

        for(size_t j = 0; j < outputs_number; j++)
        {
            if(outputs_conditions[j] == Minimum)
            {
                objective[i] += envelope(i,inputs_number+j);
            }
            else if(outputs_conditions[j] == Maximum)
            {
                objective[i] += -envelope(i,inputs_number+j);
            }
        }
    }

    const size_t optimal_index = objective.calculate_minimal_index();

    const Vector<double> optimum_values = envelope.get_row(optimal_index);

    cout << "optimal_index: " << optimal_index << endl;
    cout << "optimum_values: " << optimum_values << endl;

    return results;
}


double ResponseOptimization::calculate_random_uniform(const double& minimum, const double& maximum) const
{
  const double random = static_cast<double>(rand()/(RAND_MAX + 1.0));

  const double random_uniform = minimum + (maximum - minimum) * random;

  return random_uniform;
}

}

// OpenNN: Open Neural Networks Library.
// Copyright(C) 2005-2018 Artificial Intelligence Techniques, SL.
//
// This library is free software; you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public
// License as published by the Free Software Foundation; either
// version 2.1 of the License, or any later version.
//
// This library is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
// Lesser General Public License for more details.

// You should have received a copy of the GNU Lesser General Public
// License along with this library; if not, write to the Free Software
// Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
